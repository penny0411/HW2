# 🌤️ 智慧物聯網 HW2 - 台灣氣象預報視覺化系統

本專案已完整達成 HW2-1 至 HW2-4 的所有作業規範。

## 📋 本專案完成指標 (作業檢核清單)

### ✅ HW2-1: 獲取與觀察原始資料 (20%)
*   **關鍵程式碼**: `inspect_weather_data.py`
*   **方法**: 使用 `requests` 調用 CWA API 並利用 `json.dumps` 打印獲取的原始 JSON 結構。
*   **成果**: 成功獲取分區預報，並透過格式化輸出確認資料結構。

### ✅ HW2-2: 分析資料與提取氣溫 (20%)
*   **關鍵程式碼**: `hw2_2_verify.py`
*   **方法**: 分析 JSON 結構定位 `MinT` (最低溫) 與 `MaxT` (最高溫)，並將提取結果再次透過 `json.dumps` 展示。
*   **成果**: 精確過濾出各區域的氣溫數值，供後續資料庫儲存使用。

### ✅ HW2-3: 資料庫儲存與測試 (30%)
*   **關鍵程式碼**: `weather.py`
*   **方法**: 將提取的資料寫入 SQLite3 資料庫 (`data.db`)，資料表為 `TemperatureForecasts`。
*   **測試驗證**: 在腳本末尾加入代碼，成功查詢並於控制台輸出「中部地區」的所有氣溫資料。

### ✅ HW2-4: 網頁 Dashboard 功能改善 (30%)
*   **關鍵程式碼**: `app.py`
*   **方法**: 將資料來源由 CSV 切換為 SQLite3。
*   **視覺化介面**: 
    - **地圖模式**: 全台氣溫分佈互動地圖。
    - **趨勢模式**: 所選地區的一週最高/最低溫折線圖。
    - **數據表格**: 詳細預報清單。

---

## 🛠️ 專案執行指南

### 1. 觀察原始與提取資料 (HW2-1 & HW2-2)
```bash
# 觀察原始 JSON
python inspect_weather_data.py

# 觀察提取後的氣溫 JSON
python hw2_2_verify.py
```

### 2. 資料入庫與驗證 (HW2-3)
```bash
python weather.py
```

### 3. 啟動視覺化網頁 (HW2-4)
```bash
python -m streamlit run app.py
```

---

## 📦 技術棧
- **Language**: Python 3.14
- **Libraries**: Requests, Pandas, Streamlit, Folium, Streamlit-Folium, SQLite3
- **Data Source**: CWA Open Data Platform (F-A0010-001)
