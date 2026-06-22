import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uuid
import sqlite3
import base64
import asyncio
import sys
import io
import re
from dotenv import load_dotenv 

# --- AUDIO LIBRARY ---
from gtts import gTTS 
from google import genai
from google.genai import types

load_dotenv() 

# --- CONFIGURATION ---
MODEL_NAME = 'gemini-2.5-flash'
DB_NAME = "appointments_poc.db"

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

GEMINI_CLIENT: genai.Client | None = None

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, specialty TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY, patient_name TEXT, doctor_name TEXT, appointment_time TIMESTAMP, patient_email TEXT, status TEXT, UNIQUE(doctor_name, appointment_time))""")
    try:
        doctors = [("Dr. Meera Patel", "Cardiology"), ("Dr. Arjun Rao", "Neurology")]
        for name, spec in doctors:
            cursor.execute("INSERT OR IGNORE INTO doctors (name, specialty) VALUES (?, ?)", (name, spec))
        conn.commit()
    except: pass
    conn.close()

init_db()

# --- FASTAPI APP INITIALIZATION (FIXED) ---
app = FastAPI()

# --- TOOLS ---
def list_doctors_tool() -> dict:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, specialty FROM doctors")
    res = [{"name": r[0], "specialty": r[1]} for r in cursor.fetchall()]
    conn.close()
    return {"doctors": res}

def check_slot_tool(doctor_name: str, appointment_time: str) -> dict:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM appointments WHERE doctor_name=? AND appointment_time=?", (doctor_name, appointment_time))
    booked = cursor.fetchone()
    conn.close()
    return {"status": "booked" if booked else "available"}

def book_appointment_tool(doctor_name: str, appointment_time: str, patient_name: str, patient_email: str) -> dict:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO appointments (patient_name, doctor_name, appointment_time, patient_email, status) VALUES (?,?,?,?,?)", (patient_name, doctor_name, appointment_time, patient_email, "CONFIRMED"))
        conn.commit()
        return {"status": "success"}
    except: return {"status": "conflict"}
    finally: conn.close()

TOOL_FUNCTIONS = {
    "list_doctors": list_doctors_tool,
    "check_slot": check_slot_tool,
    "book_appointment": book_appointment_tool
}

# --- TEXT SANITIZATION ---
def clean_text_for_audio(text: str) -> str:
    # 1. Remove Markdown asterisks and hashes
    text = re.sub(r'[*_#]', '', text)
    # 2. REMOVE English translations in parentheses (e.g., "(Hello)") 
    # This prevents the agent from speaking both languages.
    text = re.sub(r'\([^)]*\)', '', text)
    return " ".join(text.split())

# --- AUDIO GENERATOR ---
async def generate_audio_gtts(text: str, lang_code: str) -> str:
    if not text: return None
    
    clean_text = clean_text_for_audio(text)
    
    try:
        lang = 'en'
        tld = 'co.in' 

        if 'hi' in lang_code: 
            lang = 'hi'
            tld = 'com' 
        elif 'te' in lang_code: 
            lang = 'te'
            tld = 'com' 
            
        def _run_gtts():
            fp = io.BytesIO()
            # slow=False creates a more natural, conversational speed
            tts = gTTS(text=clean_text, lang=lang, tld=tld, slow=False) 
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.getvalue()

        mp3_data = await asyncio.to_thread(_run_gtts)
        return base64.b64encode(mp3_data).decode('utf-8')
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        return None

# --- SYSTEM PROMPT ---
BASE_PROMPT = """
You are Sarah, a warm and caring receptionist at Apollo Hospital.

STRICT LANGUAGE POLICY:
1. Speak ONLY in the language requested by the user.
2. If the user selects Telugu, your response must be 100% Telugu script. 
3. DO NOT provide English translations or bracketed text. 
4. Avoid technical formatting like bolding (**) or bullet points.
"""

class AgentMessageRequest(BaseModel):
    session_id: str | None = None
    text: str
    language_code: str | None = "en-IN"

AGENT_SESSIONS = {}

def get_chat_session(session_id=None):
    global GEMINI_CLIENT
    if not GEMINI_CLIENT:
        GEMINI_CLIENT = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    if not session_id or session_id not in AGENT_SESSIONS:
        session_id = str(uuid.uuid4())
        AGENT_SESSIONS[session_id] = GEMINI_CLIENT.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=BASE_PROMPT,
                tools=list(TOOL_FUNCTIONS.values())
            )
        )
    return session_id, AGENT_SESSIONS[session_id]

@app.get("/")
def read_root():
    return FileResponse("frontend.html", media_type="text/html")

@app.post("/agent/new_session")
def new_session():
    sid, _ = get_chat_session()
    return {"session_id": sid}

@app.post("/agent/message")
async def agent_message(req: AgentMessageRequest):
    sid, chat = get_chat_session(req.session_id)
    
    lang_map = {
        "te-IN": "STRICT: Respond in Telugu script only. No English.",
        "hi-IN": "STRICT: Respond in Hindi script only. No English.",
        "en-IN": "Respond in English."
    }
    instruction = lang_map.get(req.language_code, "Respond in English.")
    
    try:
        response = await asyncio.to_thread(chat.send_message, f"{req.text}\n\n[Instruction: {instruction}]")
        
        while getattr(response, "function_calls", None):
            tool_responses = []
            for tool_call in response.function_calls:
                result = TOOL_FUNCTIONS[tool_call.name](**dict(tool_call.args))
                tool_responses.append(types.Part.from_function_response(name=tool_call.name, response={"result": result}))
            response = await asyncio.to_thread(chat.send_message, tool_responses)
            
        final_text = response.text
        audio_b64 = await generate_audio_gtts(final_text, req.language_code)
        
        return { "session_id": sid, "text": final_text, "audio": audio_b64 }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "session_id": sid,
            "text": f"ERROR: {str(e)}",
            "audio": None
        }

if __name__ == "__main__":
    uvicorn.run(
    app,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000))
    )