import streamlit as st
from utils.connection import get_connection


@st.cache_data
def get_seasons():

    conn = get_connection()

    query = """
        SELECT DISTINCT SEASON
        FROM SILVER.FACT_MATCH
        ORDER BY SEASON
    """

    seasons = conn.cursor().execute(query).fetchall()

    conn.close()

    return [row[0] for row in seasons]


def show_sidebar_filters():

    st.sidebar.header("🔎 Filters")

    seasons = get_seasons()

    selected_season = st.sidebar.selectbox(
        "📅 Season",
        ["All Seasons"] + seasons
    )

    return selected_season
