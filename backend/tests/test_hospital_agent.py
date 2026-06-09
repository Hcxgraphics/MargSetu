print("TEST STARTED")

from app.core.db import SessionLocal
from app.services.hospital_service import HospitalService
from app.agents.hospital_agent import HospitalAgent

db = SessionLocal()

try:
    print("Database Connected")

    service = HospitalService(db)

    print("Service Created")

    agent = HospitalAgent(service)

    print("Agent Created")

    result = agent.evaluate(patient_id=1)

    print("RESULT:")
    print(result)

except Exception as e:
    print("ERROR:")
    print(type(e).__name__)
    print(str(e))

finally:
    db.close()
    print("TEST FINISHED")