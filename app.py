import streamlit as st
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium
import os
from weather import fetch_and_save_weather

# 1. 設置網頁
st.set_page_config(page_title="台灣氣象全功能儀表板", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    .main-title { text-align: center; color: #1E3A8A; font-weight: 800; padding: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌤️ 台灣氣象預報全功能儀表板 (地圖 / 趨勢 / 表格)</h1>", unsafe_allow_html=True)

# 座標資料
REGION_COORDS = {
    "北部地區": [25.04, 121.51], "中部地區": [24.14, 120.67], "南部地區": [22.62, 120.31],
    "東北部地區": [24.75, 121.75], "東部地區": [23.97, 121.60], "東南部地區": [22.75, 121.15]
}

def get_color(temp):
    if temp < 20: return "blue"
    elif 20 <= temp < 25: return "green"
    elif 25 <= temp < 30: return "#cccc00"
    return "red"

def get_data_from_db():
    try:
        conn = sqlite3.connect("data.db")
        df = pd.read_sql_query("SELECT * FROM TemperatureForecasts", conn)
        conn.close()
        return df
    except: return None

def main():
    df = get_data_from_db()
    
    if df is None or df.empty:
        with st.spinner("⏳ 初次啟動中，正在獲取氣象資料..."):
            fetch_and_save_weather()
        df = get_data_from_db()
        if df is None or df.empty:
            st.error("⚠️ 無法獲取資料，請檢查 API Key 是否有效。")
            return

    # --- 側邊欄控制 ---
    st.sidebar.header("🎛️ 控制面板")
    
    # 1. 地區選擇 (影響折線圖與表格)
    all_regions = sorted(df["regionName"].unique())
    selected_region = st.sidebar.selectbox("📍 選擇顯示地區 (折線圖/表格)：", all_regions)
    
    # 2. 日期選擇 (影響地圖顯示)
    all_dates = sorted(df["dataDate"].unique())
    selected_date = st.sidebar.select_slider("📅 選擇地圖日期：", options=all_dates)

    # 數據篩選
    region_data = df[df["regionName"] == selected_region].sort_values("dataDate")
    date_data = df[df["dataDate"] == selected_date]

    # --- 主要佈局：左 3 右 2 ---
    col1, col2 = st.columns([3, 2])

    with col1:
        # A. 顯示地圖
        st.subheader(f"🗺️ 全台氣溫空間分佈 ({selected_date})")
        m = folium.Map(location=[23.7, 120.8], zoom_start=7, tiles="CartoDB positron")
        
        for _, row in date_data.iterrows():
            reg = row["regionName"]
            if reg in REGION_COORDS:
                avg_t = (row["mint"] + row["maxt"]) / 2
                folium.CircleMarker(
                    location=REGION_COORDS[reg],
                    radius=15, color=get_color(avg_t), fill=True, fill_color=get_color(avg_t),
                    fill_opacity=0.7,
                    popup=f"{reg}<br>平均: {avg_t}°C"
                ).add_to(m)
        
        st_folium(m, width=800, height=400, key="hybrid_map")

        # B. 顯示折線圖
        st.markdown("---")
        st.subheader(f"📈 {selected_region} 一週溫度趨勢")
        chart_df = region_data.set_index("dataDate")[["maxt", "mint"]]
        chart_df.columns = ["最高溫", "最低溫"]
        st.line_chart(chart_df)

    with col2:
        # C. 顯示詳細數據表格
        st.subheader(f"📋 {selected_region} 預報列表")
        table_df = region_data[["dataDate", "mint", "maxt"]].reset_index(drop=True)
        table_df.columns = ["日期", "最低溫 (°C)", "最高溫 (°C)"]
        st.table(table_df)
        
        # 指標卡片 (顯示今日重點)
        today_row = region_data[region_data["dataDate"] == selected_date]
        if not today_row.empty:
            st.markdown("---")
            st.subheader(f"🌡️ {selected_date} 指標")
            st.metric("當日最低溫", f"{today_row.iloc[0]['mint']}°C")
            st.metric("當日最高溫", f"{today_row.iloc[0]['maxt']}°C")

        st.info("💡 操作說明：\n1. 滑動日期軸可變動地圖氣候分布。\n2. 切換地區選單可查看該區一週趨勢圖。")

if __name__ == "__main__":
    main()
