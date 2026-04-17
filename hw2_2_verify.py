import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def verify_hw2_2():
    api_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-A0010-001"
    api_key = "CWA-031E9254-47B2-4E95-8869-7756AA1FEA2D"
    params = {"Authorization": api_key, "format": "JSON"}
    
    print("--- [HW2-2 驗證] 正在提取最高與最低氣溫資料 ---")
    
    try:
        res = requests.get(api_url, params=params, verify=False)
        data = res.json()
        
        extracted_results = []
        locations = data['records']['location']
        
        # 我們只取前兩個地區作為「觀察」範例，確保顯示內容簡潔
        for loc in locations[:2]:
            region = loc['locationName']
            # 找到 MinT 與 MaxT 的位置
            elements = {e['elementName']: e['time'] for e in loc['weatherElement']}
            
            # 提取第一天的資料作為代表
            min_t = elements['MinT'][0]['parameter']['parameterValue']
            max_t = elements['MaxT'][0]['parameter']['parameterValue']
            
            extracted_results.append({
                "地區": region,
                "分析結果": {
                    "最低氣溫 (MinT)": min_t,
                    "最高氣溫 (MaxT)": max_t
                }
            })
            
        # 使用 json.dumps 觀察提取後的資料
        print(json.dumps(extracted_results, indent=4, ensure_ascii=False))
        print("--- 驗證結束，資料提取路徑正確 ---")
        
    except Exception as e:
        # 如果 API 失效，顯示手動分析的模擬提取結果
        mock_extracted = [
            {"地區": "北部地區", "分析結果": {"最低氣溫 (MinT)": "18", "最高氣溫 (MaxT)": "25"}},
            {"地區": "中部地區", "分析結果": {"最低氣溫 (MinT)": "19", "最高氣溫 (MaxT)": "26"}}
        ]
        print(json.dumps(mock_extracted, indent=4, ensure_ascii=False))
        print(f"\n註：目前使用模擬數據展示提取邏輯 (原因: {e})")

if __name__ == "__main__":
    verify_hw2_2()
