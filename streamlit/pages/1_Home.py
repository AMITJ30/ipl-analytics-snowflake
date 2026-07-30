import streamlit as st
import pandas as pd

from utils.connection import get_connection

st.set_page_config(
    page_title="IPL Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Analytics Dashboard")

try:
    conn = get_connection()

    query = """
    SELECT *
    FROM REPORTING.VW_DASHBOARD_SUMMARY
    """

    df = pd.read_sql(query, conn)

    st.success("Data loaded successfully!")

    st.dataframe(df, use_container_width=True)

    conn.close()

except Exception as e:
    st.error(e)
