import pandas as pd

KEEP_IDS = [
    3000004,
    3000008,
    3000010,
    3000011,
    3000012,
    3000014,
    3000015,
    3000021,
    3000023,
    3000025,
    3000026,
    3000029,
    3000031,
    3000032,
    3000033,
    3000034,
    3000041,
    3000693,
    3000703,
    3000707
]

df = pd.read_csv("..\\data\\Delhi_hospitals.csv")

filtered = df[
    df["govt_hospital_id"].isin(KEEP_IDS)
]

filtered.to_csv(
    "..\\data\\margsetu_hospitals.csv",
    index=False
)

print("Saved:", len(filtered))
print(filtered[
    [
        "govt_hospital_id",
        "hospital_name"
    ]
])