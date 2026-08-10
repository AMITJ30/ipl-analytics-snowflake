import streamlit as st
import pandas as pd

from utils.connection import get_connection

st.set_page_config(
    page_title="IPL Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Analytics Dashboard")

conn = get_connection()

df = pd.read_sql(
    "SELECT * FROM REPORTING.VW_DASHBOARD_SUMMARY",
    conn
)

summary = df.iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏏 Total Matches", int(summary["TOTAL_MATCHES"]))

with col2:
    st.metric("📅 Seasons", int(summary["TOTAL_SEASONS"]))

with col3:
    st.metric("👥 Teams", int(summary["TOTAL_TEAMS"]))

with col4:
    st.metric("🧑 Players", int(summary["TOTAL_PLAYERS"]))

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("🏟️ Venues", int(summary["TOTAL_VENUES"]))

with col6:
    st.metric("🏏 Deliveries", f"{int(summary['TOTAL_DELIVERIES']):,}")

with col7:
    st.metric("🏃 Runs", f"{int(summary['TOTAL_RUNS']):,}")

with col8:
    st.metric("🎯 Wickets", f"{int(summary['TOTAL_WICKETS']):,}")

conn.close()
