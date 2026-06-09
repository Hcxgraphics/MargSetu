from sqlalchemy import text, create_engine
import os
from dotenv import load_dotenv

load_dotenv("../../backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")
engine = create_engine(DATABASE_URL)


import random   

locations = [

(28.6139,77.2090),   # CP
(28.5672,77.2100),   # AIIMS
(28.5964,77.0455),   # Dwarka
(28.7041,77.1025),   # Rohini
(28.5244,77.1855),   # Saket
(28.6448,77.3013),   # Shahdara
(28.5355,77.3910),   # Noida border
(28.6289,77.2065),   # Karol Bagh
(28.4595,77.0266),   # Gurgaon border
(28.6304,77.2177)    # New Delhi
]

with engine.begin() as conn:

    for lat,lon in locations:

        conn.execute(text("""
        INSERT INTO network_coverage
        (
            location,
            signal_strength,
            latency_ms,
            packet_loss
        )
        VALUES
        (
            ST_GeogFromText(
            'POINT('||:lon||' '||:lat||')'
            ),
            :signal,
            :latency,
            :loss
        )
        """),
        {
            "lat": lat,
            "lon": lon,
            "signal": random.randint(60,100),
            "latency": random.randint(5,40),
            "loss": round(random.uniform(0,2),2)
        })

print("Coverage inserted")