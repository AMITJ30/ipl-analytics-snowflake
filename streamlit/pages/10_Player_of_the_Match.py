import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection
from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Player of the Match",
    page_icon="🏅",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------------------------

selected_season, selected_team = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🏅 Player of the Match")

st.markdown(
    "Explore the players with the most Player-of-the-Match awards in IPL history."
)


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_player_of_match_data():

    conn = get_connection()

    query = """
        SELECT
            PLAYER_OF_MATCH,
            AWARDS_WON,
            FIRST_SEASON,
            LAST_SEASON,
            DIFFERENT_WINNING_TEAMS
        FROM IPL_ANALYTICS.REPORTING.VW_PLAYER_OF_MATCH_SUMMARY
        ORDER BY AWARDS_WON DESC
    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        "PLAYER_OF_MATCH",
        "AWARDS_WON",
        "FIRST_SEASON",
        "LAST_SEASON",
        "DIFFERENT_WINNING_TEAMS"
    ]

    df = pd.DataFrame(
        rows,
        columns=columns
    )

    cursor.close()
    conn.close()

    return df


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

try:

    df = load_player_of_match_data()

    if df.empty:

        st.warning(
            "No Player-of-the-Match data available."
        )

    else:

        # ---------------------------------------------------------------------
        # Numeric Conversion
        # ---------------------------------------------------------------------

        df["AWARDS_WON"] = pd.to_numeric(
            df["AWARDS_WON"],
            errors="coerce"
        )

        df["DIFFERENT_WINNING_TEAMS"] = pd.to_numeric(
            df["DIFFERENT_WINNING_TEAMS"],
            errors="coerce"
        )

        # ---------------------------------------------------------------------
        # Rank Players
        # ---------------------------------------------------------------------

        df = (
            df
            .sort_values(
                "AWARDS_WON",
                ascending=False
            )
            .reset_index(drop=True)
        )

        df["PLAYER_RANK"] = (
            df.index + 1
        )

        # =====================================================================
        # KPI CARDS
        # =====================================================================

        top_player = df.iloc[0]

        total_players = len(df)

        total_awards = int(
            df["AWARDS_WON"].sum()
        )

        highest_awards = int(
            top_player["AWARDS_WON"]
        )

        # ---------------------------------------------------------------------
        # KPI Section
        # ---------------------------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🏆 Most Awards",
                top_player["PLAYER_OF_MATCH"]
            )

        with col2:

            st.metric(
                "🏅 Awards Won",
                highest_awards
            )

        with col3:

            st.metric(
                "👥 Total Players",
                total_players
            )

        with col4:

            st.metric(
                "🏅 Total Awards",
                f"{total_awards:,}"
            )

        st.divider()

        # =====================================================================
        # TOP 10 PLAYERS
        # =====================================================================

        st.subheader(
            "🏆 Top 10 Player-of-the-Match Award Winners"
        )

        top_10 = (
            df
            .sort_values(
                "AWARDS_WON",
                ascending=False
            )
            .head(10)
            .sort_values(
                "AWARDS_WON"
            )
        )

        fig = px.bar(
            top_10,
            x="AWARDS_WON",
            y="PLAYER_OF_MATCH",
            orientation="h",
            text="AWARDS_WON",
            title="Top 10 Player-of-the-Match Award Winners"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Awards Won",
            yaxis_title="Player",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================================================
        # AWARDS VS DIFFERENT WINNING TEAMS
        # =====================================================================

        st.subheader(
            "🏏 Awards vs Different Winning Teams"
        )

        scatter_df = (
            df
            .dropna(
                subset=[
                    "AWARDS_WON",
                    "DIFFERENT_WINNING_TEAMS"
                ]
            )
            .copy()
        )

        fig_scatter = px.scatter(
            scatter_df,
            x="DIFFERENT_WINNING_TEAMS",
            y="AWARDS_WON",
            size="AWARDS_WON",
            hover_name="PLAYER_OF_MATCH",
            hover_data=[
                "FIRST_SEASON",
                "LAST_SEASON"
            ],
            title="Player-of-the-Match Awards vs Different Winning Teams"
        )

        fig_scatter.update_layout(
            xaxis_title="Different Winning Teams",
            yaxis_title="Awards Won"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

        # =====================================================================
        # PLAYER LEADERBOARD
        # =====================================================================

        st.subheader(
            "📊 Player-of-the-Match Leaderboard"
        )

        # Only Top 10
        display_df = (
            df
            .sort_values(
                "PLAYER_RANK"
            )
            .head(10)
            .copy()
        )

        display_df = display_df.rename(
            columns={
                "PLAYER_RANK": "Rank",
                "PLAYER_OF_MATCH": "Player",
                "AWARDS_WON": "Awards Won",
                "FIRST_SEASON": "First Season",
                "LAST_SEASON": "Last Season",
                "DIFFERENT_WINNING_TEAMS": "Different Winning Teams"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# -----------------------------------------------------------------------------
# Error Handling
# -----------------------------------------------------------------------------

except Exception as e:

    st.error(
        "❌ Unable to load Player-of-the-Match data."
    )

    st.code(
        str(e)
    )
