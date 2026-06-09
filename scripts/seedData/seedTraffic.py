from sqlalchemy import text, create_engine
import os
from dotenv import load_dotenv

load_dotenv("../../backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")
engine = create_engine(DATABASE_URL)


import random   

roads = [
    "Ring Road",
    "Outer Ring Road",
    "NH-48",
    "Mathura Road",
    "MG Road",
    "Noida Link Road",
    "Dwarka Expressway",
    "Rohini Road",
    "Vikas Marg",
    "GT Karnal Road"
]

with engine.begin() as conn:

    for road in roads:

        congestion = random.randint(10,100)

        avg_speed = max(
            10,
            80 - congestion
        )

        conn.execute(text("""
        INSERT INTO traffic_data
        (
            road_segment,
            avg_speed,
            congestion_score
        )
        VALUES
        (
            :road,
            :speed,
            :congestion
        )
        """),
        {
            "road": road,
            "speed": avg_speed,
            "congestion": congestion
        })

print("Traffic inserted")