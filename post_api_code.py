import json
import pandas as pd
import os
from dotenv import load_dotenv
import requests
from typing import TypedDict, List
load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
url = "http://3.216.182.112:8000/api/agencies"
df = pd.read_excel("rankglobal_agencies_data.xlsx")
df = df.where(pd.notna(df), "none")
records = df.to_dict(orient="records")

with open("rankglobal_companies.json","w", encoding="utf-8") as f:
    json.dump(records,f,indent=2, ensure_ascii=False)
import math

def sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
    return obj

data = records[1]
print(data)
payload = {
    "name" : data.get("company_name", ""),
    "description": data.get("description", ""),
    "email": "info@66degrees.com",
    "logo_url": data.get("logo_url", ""),
    "website": data.get("website_url", ""),
    "category_ids": str(data.get("category_ids", "")).split("|"),
    "location": data.get("location",""),
    "team_size": data.get("team_size",""),
    "technologies": str(data.get("technologies_used","")).split("|"),
    "budget_range":"10k-15k"
}
payload = sanitize_for_json(payload)



headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(
    url,
    json=payload,
    headers=headers
)
print(response.json)



# payload_2 = {
#     "search": "Relative"
# }
# response_2 = requests.get(
#     url,
#     params=payload_2,
#     headers=headers
# )
# print(response_2.json())