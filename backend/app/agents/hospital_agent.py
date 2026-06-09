from datetime import datetime

from app.services.hospital_service import HospitalService


class HospitalAgent:

    def __init__(
        self,
        hospital_service: HospitalService
    ):
        self.hospital_service = hospital_service

    @staticmethod
    def normalize(
        value: float,
        max_value: float
    ) -> float:

        if max_value <= 0:
            return 0.0

        return value / max_value

    @staticmethod
    def min_max_normalize(
        value: float,
        min_value: float,
        max_value: float
    ) -> float:

        if max_value == min_value:
            return 0.5

        return (
            (value - min_value)
            /
            (max_value - min_value)
        )

    @staticmethod
    def clamp(
        value,
        minimum=0.0,
        maximum=1.0
    ):
        return max(
            minimum,
            min(value, maximum)
        )

    def calculate_bed_score(
        self,
        triage_level: str,
        critical_score: float,
        non_critical_score: float
    ) -> float:

        triage_level = (
            triage_level.upper()
            if triage_level
            else "GREEN"
        )

        if triage_level == "RED":

            return (
                0.7 * critical_score
                +
                0.3 * non_critical_score
            )

        elif triage_level == "YELLOW":

            return (
                0.4 * critical_score
                +
                0.6 * non_critical_score
            )

        return non_critical_score

    def is_rejected(
        self,
        emergency_type: str,
        hospital
    ) -> bool:

        critical_cases = {
            "Cardiac Arrest",
            "Respiratory Failure"
        }

        return (
            emergency_type in critical_cases
            and
            hospital.available_critical_with_vent == 0
        )

    def calculate_freshness_score(
        self,
        last_update
    ):

        if not last_update:
            return 0.0

        days_old = (
            datetime.utcnow()
            -
            last_update
        ).days

        freshness_score = (
            1 - days_old/180
        )

        return self.clamp(
            freshness_score
        )

    def evaluate(
        self,
        patient_id: int
    ):

        patient = (
            self.hospital_service
            .get_patient(patient_id)
        )

        if not patient:
            raise ValueError(
                f"Patient {patient_id} not found"
            )

        hospitals = (
            self.hospital_service
            .get_all_hospitals()
        )

        if not hospitals:
            return []

        max_non_critical = max(
            h.available_non_critical
            for h in hospitals
        )

        max_critical = max(
            (
                h.available_critical_without_vent
                +
                h.available_critical_with_vent
            )
            for h in hospitals
        )

        max_queue = max(
            h.er_queue
            for h in hospitals
        )

        min_readiness = min(
            h.readiness_score
            for h in hospitals
        )

        max_readiness = max(
            h.readiness_score
            for h in hospitals
        )

        results = []

        for hospital in hospitals:

            if self.is_rejected(
                patient.emergency_type,
                hospital
            ):
                continue

            critical_beds = (
                hospital.available_critical_without_vent
                +
                hospital.available_critical_with_vent
            )

            # RED patients require critical beds

            if (
                patient.triage_level == "RED"
                and
                critical_beds == 0
            ):
                continue

            critical_score = (
                self.normalize(
                    critical_beds,
                    max_critical
                )
            )

            non_critical_score = (
                self.normalize(
                    hospital.available_non_critical,
                    max_non_critical
                )
            )

            queue_score = self.clamp(
                1 -
                self.normalize(
                    hospital.er_queue,
                    max_queue
                )
            )

            readiness_score = (
                self.min_max_normalize(
                    hospital.readiness_score,
                    min_readiness,
                    max_readiness
                )
            )

            freshness_score = (
                self.calculate_freshness_score(
                    hospital.last_update
                )
            )

            bed_score = (
                self.calculate_bed_score(
                    patient.triage_level,
                    critical_score,
                    non_critical_score
                )
            )

            # FINAL FORMULA

            hospital_score = (
                0.45 * bed_score
                +
                0.15 * queue_score
                +
                0.25 * readiness_score
                +
                0.15 * freshness_score
            )

            results.append(
                {
                    "hospital_id":
                        hospital.govt_hospital_id,

                    "hospital":
                        hospital.hospital_name,

                    "hospital_score":
                        round(
                            hospital_score,
                            4
                        ),

                    "critical_beds":
                        critical_beds,

                    "non_critical_beds":
                        hospital.available_non_critical,

                    "bed_score": round(bed_score, 4),

                    "queue":
                        hospital.er_queue,

                    "readiness":
                        hospital.readiness_score,

                    "critical_score":
                        round(critical_score, 4),

                    "queue_score":
                        round(
                            queue_score,
                            4
                        ),

                    "readiness_score":
                        round(
                            readiness_score,
                            4
                        ),

                    "freshness_score":
                        round(
                            freshness_score,
                            4
                        )
                }
            )

        results.sort(
            key=lambda x:
            x["hospital_score"],
            reverse=True
        )

        return results