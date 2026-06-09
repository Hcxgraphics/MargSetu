from sqlalchemy import text, create_engine
import os
from dotenv import load_dotenv

load_dotenv("../../backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")
engine = create_engine(DATABASE_URL)


import random   

sexes = ["Male","Female"]

emergencies = [
    "Cardiac Arrest",
    "Stroke",
    "Accident",
    "Trauma",
    "Burn Injury",
    "Respiratory Failure"
]

triage = [
    "GREEN",
    "YELLOW",
    "ORANGE",
    "RED"
]

with engine.begin() as conn:

    for _ in range(30):

        conn.execute(text("""
        INSERT INTO patients
        (
            age,
            sex,
            emergency_type,
            triage_level
        )
        VALUES
        (
            :age,
            :sex,
            :etype,
            :triage
        )
        """),
        {
            "age": random.randint(18,90),
            "sex": random.choice(sexes),
            "etype": random.choice(emergencies),
            "triage": random.choice(triage)
        })

print("Patients inserted")