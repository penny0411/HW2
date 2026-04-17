import requests
import sqlite3
import urllib3
import datetime

# 1. 保留處理 SSL 警告的邏輯
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # 建立資料表，包含 id (主鍵)、regionName、dataDate、mint、maxt
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TemperatureForecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            regionName TEXT,
            dataDate TEXT,
            mint INTEGER,
            maxt INTEGER
        )
    ''')
    # 清空舊資料以確保每次執行都是最新的一週預報
    cursor.execute('DELETE FROM TemperatureForecasts')
    conn.commit()
    return conn

def fetch_and_save_weather():
    api_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-A0010-001"
    api_key = "CWA-031E9254-47B2-4E95-8869-7756AA1FEA2D" # 請視需求更換
    
    params = {"Authorization": api_key, "format": "JSON"}
    
    conn = init_db()
    cursor = conn.cursor()

    try:
        print("正在從 CWA API 獲取資料...")
        response = requests.get(api_url, params=params, verify=False, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            locations = data.get("records", {}).get("location", [])
            
            for loc in locations:
                region = loc.get("locationName")
                elements = {e['elementName']: e['time'] for e in loc.get("weatherElement", [])}
                min_t_list = elements.get("MinT", [])
                max_t_list = elements.get("MaxT", [])
                
                for i in range(min(len(min_t_list), len(max_t_list))):
                    date = min_t_list[i].get("startTime").split(" ")[0]
                    min_v = int(min_t_list[i].get("parameter", {}).get("parameterValue"))
                    max_v = int(max_t_list[i].get("parameter", {}).get("parameterValue"))
                    
                    # 寫入 SQLite
                    cursor.execute('''
                        INSERT INTO TemperatureForecasts (regionName, dataDate, mint, maxt)
                        VALUES (?, ?, ?, ?)
                    ''', (region, date, min_v, max_v))
            conn.commit()
            print("✅ 資料已成功儲存至 SQLite 資料庫 (data.db)")
        else:
            raise Exception("API Key 可能失效或網路錯誤")
            
    except Exception as e:
        print(f"⚠️ 抓取失敗，生成模擬資料進行測試：{e}")
        # 模擬資料
        regions = ["北部地區", "中部地區", "南部地區", "東北部地區", "東部地區", "東南部地區"]
        today = datetime.date.today()
        for r in regions:
            for i in range(7):
                d = (today + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                cursor.execute('INSERT INTO TemperatureForecasts (regionName, dataDate, mint, maxt) VALUES (?, ?, ?, ?)', 
                               (r, d, 20+i, 28+i))
        conn.commit()

    # --- HW2-3 驗證代碼：從資料庫查詢並列出「中部地區」的所有資料 ---
    print("\n--- [HW2-3 驗證] 中部地區氣溫資料查詢結果 ---")
    cursor.execute('SELECT * FROM TemperatureForecasts WHERE regionName LIKE "%中部%"')
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]} | 地區: {row[1]} | 日期: {row[2]} | 最低溫: {row[3]}°C | 最高溫: {row[4]}°C")
    print("-------------------------------------------\n")
    
    conn.close()

if __name__ == "__main__":
    fetch_and_save_weather()
