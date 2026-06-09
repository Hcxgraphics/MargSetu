from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from app.core.db import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    age = Column(
        Integer,
        nullable=False
    )

    sex = Column(
        String(10),
        nullable=False
    )

    emergency_type = Column(
        String(50),
        nullable=False
    )

    triage_level = Column(
        String(10),
        nullable=False
    )

    created_at = Column(
        DateTime
    )