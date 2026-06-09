from sqlalchemy.orm import Session

from app.models.hospital import Hospital
from app.models.patient import Patient


class HospitalService:

    def __init__(self, db: Session):
        self.db = db

    def get_patient(
        self,
        patient_id: int
    ):
        return (
            self.db.query(Patient)
            .filter(
                Patient.patient_id == patient_id
            )
            .first()
        )

    def get_all_hospitals(self):
        return (
            self.db.query(Hospital)
            .all()
        )

    def get_hospital_by_id(
        self,
        hospital_id: int
    ):
        return (
            self.db.query(Hospital)
            .filter(
                Hospital.govt_hospital_id
                == hospital_id
            )
            .first()
        )