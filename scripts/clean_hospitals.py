import pandas as pd
import random
from datetime import datetime

# ==========================================
# CONFIG
# ==========================================

INPUT_CSV = "../data/delhi_hospitals_raw.csv"
OUTPUT_CSV = "../data/Delhi_hospitals.csv"

# ==========================================
# LOAD RAW DATA
# ==========================================

df = pd.read_csv(INPUT_CSV)

print(f"Loaded {len(df)} hospitals")

# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

df.columns = [col.strip() for col in df.columns]

# ==========================================
# RENAME COLUMNS
# ==========================================

df = df.rename(
    columns={
        "Hospital ID": "govt_hospital_id",
        "Hospital Name": "hospital_name",
        "Available Free Non-Critical Bed":
            "available_non_critical",
        "Available Free Critical Bed (without ventilator)":
            "available_critical_without_vent",
        "Available Free Critical Bed (with ventilator)":
            "available_critical_with_vent",
        "Hospital Phone no.":
            "hospital_phone",
        "Last Update Date":
            "last_update"
    }
)

# ==========================================
# KEEP REQUIRED COLUMNS
# ==========================================

required_cols = [
    "govt_hospital_id",
    "hospital_name",
    "available_non_critical",
    "available_critical_without_vent",
    "available_critical_with_vent",
    "hospital_phone",
    "last_update"
]

df = df[required_cols]

# ==========================================
# CLEAN NUMERIC COLUMNS
# ==========================================

numeric_cols = [
    "available_non_critical",
    "available_critical_without_vent",
    "available_critical_with_vent"
]

for col in numeric_cols:

    df[col] = (
        pd.to_numeric(
            df[col],
            errors="coerce"
        )
        .fillna(0)
        .astype(int)
    )

    # remove negative values
    df[col] = df[col].clip(lower=0)

# ==========================================
# SYNTHETIC ER QUEUE
# ==========================================

random.seed(42)

df["er_queue"] = [
    random.randint(0, 30)
    for _ in range(len(df))
]

# ==========================================
# READINESS SCORE
# ==========================================

df["readiness_score"] = (
    df["available_non_critical"] * 1
    + df["available_critical_without_vent"] * 3
    + df["available_critical_with_vent"] * 5
    - df["er_queue"]
)

# ==========================================
# PLACEHOLDER COORDINATES
# ==========================================

df["latitude"] = None
df["longitude"] = None

# ==========================================
# REORDER COLUMNS
# ==========================================

final_columns = [
    "govt_hospital_id",
    "hospital_name",
    "latitude",
    "longitude",
    "available_non_critical",
    "available_critical_without_vent",
    "available_critical_with_vent",
    "er_queue",
    "hospital_phone",
    "readiness_score",
    "last_update"
]

df = df[final_columns]

# ==========================================
# SAVE
# ==========================================

df.to_csv(
    OUTPUT_CSV,
    index=False
)

print(f"\nSaved -> {OUTPUT_CSV}")
print(df.head())
print("\nShape:", df.shape)