import streamlit as st
import pandas as pd

from utils.connection import get_connection

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Analytics Dashboard")

conn = get_connection()

query = """
SELECT *
FROM REPORTING.VW_DASHBOARD_SUMMARY;
"""

df = pd.read_sql(query, conn)

conn.close()

st.dataframe(df, use_container_width=True)