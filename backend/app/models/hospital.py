from sqlalchemy import (Column,Integer,String,Float,DateTime)
from app.core.db import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    govt_hospital_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    hospital_name = Column(
        String(255),
        nullable=False
    )

    latitude = Column(
        Float,
        nullable=False
    )

    longitude = Column(
        Float,
        nullable=False
    )

    available_non_critical = Column(
        Integer,
        nullable=False,
        default=0
    )

    available_critical_without_vent = Column(
        Integer,
        nullable=False,
        default=0
    )

    available_critical_with_vent = Column(
        Integer,
        nullable=False,
        default=0
    )

    er_queue = Column(
        Integer,
        nullable=False,
        default=0
    )

    hospital_phone = Column(
        String(50)
    )

    readiness_score = Column(
        Float,
        nullable=False,
        default=0.0
    )

    last_update = Column(
        DateTime
    )