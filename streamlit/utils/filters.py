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

    cursor = conn.cursor()
    cursor.execute(query)

    seasons = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row[0] for row in seasons]


@st.cache_data
def get_teams():

    conn = get_connection()

    query = """
        SELECT DISTINCT TEAM
        FROM (
            SELECT TEAM1 AS TEAM
            FROM SILVER.FACT_MATCH

            UNION

            SELECT TEAM2 AS TEAM
            FROM SILVER.FACT_MATCH
        )
        WHERE TEAM IS NOT NULL
        ORDER BY TEAM
    """

    cursor = conn.cursor()
    cursor.execute(query)

    teams = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row[0] for row in teams]


def show_sidebar_filters():

    st.sidebar.header("🔎 Filters")

    seasons = get_seasons()

    selected_season = st.sidebar.selectbox(
        "📅 Season",
        ["All Seasons"] + seasons,
        key="global_season"
    )

    teams = get_teams()

    selected_team = st.sidebar.selectbox(
        "👥 Team",
        ["All Teams"] + teams,
        key="global_team"
    )

    return selected_season, selected_team
