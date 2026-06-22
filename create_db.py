import sqlite3

conn = sqlite3.connect("appointments_poc.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE doctors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    specialty TEXT
)
""")

cursor.execute("""
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    patient_name TEXT,
    doctor_name TEXT,
    appointment_time TEXT,
    patient_email TEXT,
    status TEXT,
    UNIQUE(doctor_name, appointment_time)
)
""")

cursor.execute(
    "INSERT INTO doctors (name, specialty) VALUES (?, ?)",
    ("Dr. Meera Patel", "Cardiology")
)

cursor.execute(
    "INSERT INTO doctors (name, specialty) VALUES (?, ?)",
    ("Dr. Arjun Rao", "Neurology")
)

conn.commit()
conn.close()

print("Database created")