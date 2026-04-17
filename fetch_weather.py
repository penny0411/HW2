import requests
import pandas as pd
import os
import datetime
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 設定
API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-A0010-001"
API_KEY = "CWA-031E9254-47B2-4E95-8869-7756AA1FEA2D" # 請替換成您自己的 API KEY

def fetch_weather_data(api_key):
    params = {"Authorization": api_key, "format": "JSON"}
    try:
        response = requests.get(API_URL, params=params, verify=False, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        records = []
        locations = data.get("records", {}).get("location", [])
        
        for loc in locations:
            region = loc.get("locationName")
            elements = {e.get("elementName"): e.get("time", []) for e in loc.get("weatherElement", [])}
            
            min_list = elements.get("MinT", [])
            max_list = elements.get("MaxT", [])
            
            for i in range(min(len(min_list), len(max_list))):
                date = min_list[i].get("startTime").split(" ")[0]
                min_v = int(min_list[i].get("parameter", {}).get("parameterValue"))
                max_v = int(max_list[i].get("parameter", {}).get("parameterValue"))
                records.append({
                    "Region": region,
                    "Date": date,
                    "MinTemp": min_v,
                    "MaxTemp": max_v,
                    "AvgTemp": (min_v + max_v) / 2
                })
        return records
    except Exception as e:
        print(f"API Fetch Error: {e}")
        return None

def main():
    api_key = os.getenv("CWA_API_KEY", API_KEY)
    weather_records = fetch_weather_data(api_key)
    
    if weather_records:
        df = pd.DataFrame(weather_records)
        print("Successfully fetched data from CWA.")
    else:
        print("Generating mock data for demonstration...")
        regions = ["北部", "中部", "南部", "東北部", "東部", "東南部"]
        today = datetime.date.today()
        records = []
        import random
        for r in regions:
            for i in range(7):
                date = (today + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                min_v = random.randint(15, 22)
                max_v = min_v + random.randint(5, 10)
                records.append({
                    "Region": r,
                    "Date": date,
                    "MinTemp": min_v,
                    "MaxTemp": max_v,
                    "AvgTemp": (min_v + max_v) / 2
                })
        df = pd.DataFrame(records)

    df.to_csv("weather_data.csv", index=False, encoding="utf-8-sig")
    print("Data saved to weather_data.csv")

if __name__ == "__main__":
    main()
