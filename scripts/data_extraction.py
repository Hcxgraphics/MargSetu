import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://dshm.delhi.gov.in/mis/Private/frmFreeBedMonitoringReport.aspx"

response = requests.get(
    url,
    verify=False,   # Delhi govt SSL certificate issue
    timeout=30
)

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find(
    "table",
    {"id": "ctl00_ContentPlaceHolder1_grvHospital"}
)

rows = []

for tr in table.find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all(["th","td"])]
    rows.append(cols)

df = pd.DataFrame(rows[1:], columns=rows[0])

df.to_csv(
    "../data/delhi_hospitals_raw.csv",
    index=False
)

print(df.head())
print(df.shape)