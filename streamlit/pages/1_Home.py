import streamlit as st
import pandas as pd

from utils.connection import get_connection

st.set_page_config(
    page_title="IPL Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Dashboard")

conn = get_connection()

query = """
SELECT *
FROM VW_DASHBOARD_SUMMARY
"""

df = pd.read_sql(query, conn)

st.dataframe(df)

conn.close()
