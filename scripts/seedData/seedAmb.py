from sqlalchemy import text, create_engine
import os
from dotenv import load_dotenv

load_dotenv("../../backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")
engine = create_engine(DATABASE_URL)


import random   
ambulances = []

locations = [
    (28.6139,77.2090),  # CP
    (28.7041,77.1025),  # Rohini
    (28.5355,77.3910),  # Noida
    (28.5964,77.0455),  # Dwarka
    (28.6448,77.3013),  # Shahdara
    (28.5244,77.1855),  # Saket
    (28.6507,77.2334),  # ISBT
    (28.5672,77.2100),  # AIIMS
]

for i in range(1,21):

    lat,lon = random.choice(locations)

    ambulances.append({
        "code":f"AMB{i:03}",
        "lat":lat,
        "lon":lon,
        "speed":random.randint(0,60),
        "status":random.choice([
            "AVAILABLE",
            "BUSY",
            "RETURNING"
        ])
    })

with engine.begin() as conn:

    for a in ambulances:

        conn.execute(text("""
        INSERT INTO ambulances
        (
        ambulance_code,
        current_location,
        speed,
        status
        )

        VALUES
        (
        :code,
        ST_GeogFromText(
        'POINT('||:lon||' '||:lat||')'
        ),
        :speed,
        :status
        )
        """),a)

print("20 ambulances inserted")