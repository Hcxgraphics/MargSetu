class TrafficAgent:

    def score(
        self,
        avg_speed,
        congestion
    ):

        speed_score = min(
            avg_speed/60,
            1
        )

        congestion_score = (
            1 -
            min(congestion/100,1)
        )

        return (
            0.6*speed_score +
            0.4*congestion_score
        )