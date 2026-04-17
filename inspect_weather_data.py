import requests
import json
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 設定 CWA API
# 您可以使用現有的 Authorization Key
API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-A0010-001"
API_KEY = "CWA-031E9254-47B2-4E95-8869-7756AA1FEA2D"

def inspect_data():
    print(f"正在連線至 CWA API: {API_URL}")
    
    params = {
        "Authorization": API_KEY,
        "format": "JSON"
    }
    
    try:
        # 使用 requests 調用 API
        response = requests.get(API_URL, params=params, verify=False)
        response.raise_for_status()
        
        # 獲取 JSON 資料
        data = response.json()
        
        # 觀察獲得的資料結構 (使用 json.dumps 並設定縮排與字碼)
        # indent=4 讓結構更容易閱讀，ensure_ascii=False 確保中文正常顯示
        formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
        
        print("\n--- 觀察 JSON 資料結構 開始 ---")
        # 為了避免控制台文字過多，我們先顯示前 2000 個字元
        print(formatted_json[:2000] + "\n... (資料過長，僅顯示部分內容) ...")
        print("--- 觀察 JSON 資料結構 結束 ---\n")
        
        # 檢查主要的欄位
        if "records" in data:
            print(f"成功獲取資料！")
            print(f"資料來源: {data['records']['datasetDescription']}")
            print(f"包含地區數量: {len(data['records']['location'])}")
            
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    inspect_data()
