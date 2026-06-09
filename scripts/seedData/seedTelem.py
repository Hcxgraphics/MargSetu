from sqlalchemy import text, create_engine
import os
from dotenv import load_dotenv

load_dotenv("../../backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")
engine = create_engine(DATABASE_URL)


import random   
with engine.begin() as conn:

    for _ in range(50):

        conn.execute(text("""
        INSERT INTO telemetry
        (
            ambulance_id,
            patient_id,
            heart_rate,
            spo2,
            respiratory_rate,
            signal_strength
        )
        VALUES
        (
            :ambulance,
            :patient,
            :hr,
            :spo2,
            :rr,
            :signal
        )
        """),
        {
            "ambulance": random.randint(1,15),
            "patient": random.randint(1,30),
            "hr": random.randint(60,140),
            "spo2": random.randint(80,100),
            "rr": random.randint(12,35),
            "signal": random.randint(50,100)
        })

print("Telemetry inserted")