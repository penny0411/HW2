# 🌤️ 智慧物聯網 HW2 - 台灣氣象預報視覺化系統

本專案旨在建構一個完整的氣象數據處理流程，包含從 CWA API 獲取資料、預處理、儲存至 SQL 資料庫，最後以互動式 Web App (Streamlit) 呈現空間分佈與時間趨勢。

## 📋 專案開發總結

根據作業規範與需求，本專案已完成以下功能開發：

### 1. 資料抓取與觀察 (Initial Setup)
*   **API 串接**：使用 `requests` 調用 CWA API (`F-A0010-001`) 獲取台灣六大區域之一週預報。
*   **結構觀察**：建立 `inspect_weather_data.py`，利用 `json.dumps` 格式化輸出資料結構，以便理解 JSON 嵌套層次。
*   **SSL 處理**：程式具備自動忽略 SSL 安全憑證警告的功能，確保在各種網路環境下皆能穩定運行。

### 2. 資料庫管理 (HW2-3 規範)
*   **技術選型**：將資料儲存方式從 CSV 升級為 **SQLite3** 關聯式資料庫。
*   **資料庫名稱**：`data.db`。
*   **資料表設計**：
    *   `TemperatureForecasts` (欄位：id, regionName, dataDate, mint, maxt)。
*   **自動化驗證**：在 `weather.py` 執行結束前，會自動查詢並列出「中部地區」的所有預報結果，以驗證資料存入成功。

### 3. Web App 互動視覺化 (HW2-4 混合版)
*   **混合式佈局**：採用左右並行佈局 (Left-Right Layout)，整合地圖、圖表與表格。
*   **互動功能**：
    *   **互動地圖**：依據選取的日期，於台灣地圖上顯示各地區之標記，並根據 **平均溫** 顯示顏色 (藍: <20°C, 綠: 20-25°C, 黃: 25-30°C, 紅: >30°C)。
    *   **地區選擇器**：透過下拉選單切換地區。
    *   **溫度趨勢折線圖**：針對所選地區顯示一週內的最高溫與最低溫變化趨勢。
    *   **數據表格**：即時顯示與圖表對應的詳細數值數據。

---

## 🛠️ 檔案結構說明
| 檔案名稱 | 說明 |
| :--- | :--- |
| `weather.py` | 核心抓取程式 (資料庫版) |
| `app.py` | 全功能視覺化儀表板程式 |
| `inspect_weather_data.py` | JSON 資料結構觀察工具 |
| `data.db` | SQLite 資料庫檔案 |
| `requirements.txt` | 專案所需 Python 套件清單 |

---

## 🚀 如何執行

### 1. 安裝環境
請確保已安裝相關套件：
```bash
pip install requests pandas streamlit folium streamlit-folium sqlite3
```

### 2. 資料更新與驗證 (HW2-3)
執行此程式獲取最新預報並觀察終端機的「中部地區」驗證輸出：
```bash
python weather.py
```

### 3. 啟動視覺化網頁 (HW2-4)
```bash
python -m streamlit run app.py
```
啟動後請至 [http://localhost:8501](http://localhost:8501) 開啟網頁。
