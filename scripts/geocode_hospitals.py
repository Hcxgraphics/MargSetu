import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

INPUT_CSV = "..\\data\\Delhi_hospitals.csv"


df = pd.read_csv(INPUT_CSV)
geolocator = Nominatim(
    user_agent="margsetu_hospital_geocoder"
)

geocode = RateLimiter(
    geolocator.geocode,
    min_delay_seconds=1
)

for idx, row in df.iterrows():

    # Skip if already filled
    if pd.notna(row["latitude"]) and pd.notna(row["longitude"]):
        continue

    hospital_name = str(row["hospital_name"])

    query = f"{hospital_name}, Delhi, India"

    print(f"\n[{idx+1}/{len(df)}] Searching:")
    print(query)

    try:
        location = geocode(query)

        if location:

            df.at[idx, "latitude"] = location.latitude
            df.at[idx, "longitude"] = location.longitude

            print(
                f"Found: "
                f"{location.latitude}, "
                f"{location.longitude}"
            )

        else:
            print("Not Found")

    except Exception as e:
        print("Error:", e)

    # Save after every row
    df.to_csv(INPUT_CSV, index=False)

    time.sleep(1)


df.to_csv(INPUT_CSV, index=False)

print("\nFinished!")
print(
    df[["hospital_name",
        "latitude",
        "longitude"]].head()
)