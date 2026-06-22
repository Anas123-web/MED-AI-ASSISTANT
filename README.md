# 🏥 MED AI ASSISTANT

An AI-powered Hospital Appointment Booking Assistant built using FastAPI, Google Gemini, SQLite, HTML, JavaScript, and Tailwind CSS.

The application acts as a virtual hospital receptionist named **Sarah**, capable of:

* Booking appointments
* Checking doctor availability
* Providing multilingual conversations
* Managing appointment records
* Generating voice responses
* Handling hospital-related patient interactions

---

# 🚀 Features

✅ AI-Powered Hospital Receptionist

✅ Appointment Booking System

✅ Doctor Availability Checking

✅ SQLite Database Integration

✅ Voice-Based Interaction

✅ Multilingual Support

* English
* Hindi
* Telugu

✅ Gemini AI Integration

✅ Modern Responsive UI

---

# 🛠️ Tech Stack

## Frontend

* HTML5
* Tailwind CSS
* JavaScript
* Web Speech API

## Backend

* FastAPI
* Python

## AI

* Google Gemini

## Database

* SQLite

## Voice

* gTTS (Google Text-to-Speech)

---

# 📂 Project Structure

```text
MED-AI-ASSISTANT/
│
├── app.py
├── frontend.html
├── requirements.txt
├── appointments_poc.db
├── .env
├── README.md
└── .gitignore
```

---

# ⚙️ How the System Works

```text
User
 │
 ▼
Frontend (HTML + JS)
 │
 ▼
FastAPI Backend
 │
 ├── Gemini AI
 │
 ├── SQLite Database
 │
 └── gTTS Voice Generation
 │
 ▼
Response to User
```

---

# 🧠 Workflow

### Step 1

User enters:

* Name
* Email
* Language

### Step 2

User clicks:

```text
Start Voice Call
```

### Step 3

Browser captures voice using:

```javascript
SpeechRecognition
```

### Step 4

Voice is converted into text.

### Step 5

Text is sent to FastAPI backend.

### Step 6

Gemini processes the request.

### Step 7

Backend checks:

* Doctors
* Appointment slots
* Existing bookings

### Step 8

Appointment is stored in SQLite.

### Step 9

Gemini generates a response.

### Step 10

gTTS converts response into audio.

### Step 11

Audio is played back to the user.

---

# 🗄️ Database Design

## Doctors Table

```sql
CREATE TABLE doctors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    specialty TEXT
);
```

## Appointments Table

```sql
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    patient_name TEXT,
    doctor_name TEXT,
    appointment_time TIMESTAMP,
    patient_email TEXT,
    status TEXT
);
```

---

# 👨‍⚕️ Default Doctors

```text
Dr. Meera Patel
Specialty: Cardiology

Dr. Arjun Rao
Specialty: Neurology
```

---

# 🔑 Environment Variables

Create a file:

```text
.env
```

Add:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Get API Key from:

https://aistudio.google.com/app/apikey

---

# 📦 Installation Guide

## Clone Repository

```bash
git clone https://github.com/Anas123-web/MED-AI-ASSISTANT.git

cd MED-AI-ASSISTANT
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

## Method 1

```bash
python app.py
```

## Method 2

```bash
uvicorn app:app --reload
```

Open:

```text
http://localhost:8000
```

---

# 🌐 Deployment

## Render Deployment

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

Add Environment Variable:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

---

# 🔮 Future Enhancements

* Email Notifications
* SMS Notifications
* Doctor Dashboard
* Patient Dashboard
* PostgreSQL Database
* JWT Authentication
* Appointment History
* Docker Support
* Cloud Storage
* Hospital Admin Panel

---

# 📈 Learning Outcomes

This project demonstrates:

* FastAPI Development
* REST APIs
* Google Gemini Integration
* Prompt Engineering
* Database Design
* Full Stack Development
* AI Agent Workflows
* Voice Interfaces
* Deployment

---

# 👨‍💻 Author

Mohammad Anas

GitHub:
https://github.com/Anas123-web

LinkedIn:
https://www.linkedin.com/in/anas-mohammad-594985258/

---

# ⭐ Support

If you found this project useful, please give it a star on GitHub.
