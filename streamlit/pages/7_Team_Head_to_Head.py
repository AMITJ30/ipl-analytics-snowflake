import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.connection import get_connection
from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Team Head-to-Head",
    page_icon="🤝",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------------------------

selected_season, selected_team = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🤝 Team Head-to-Head")

st.markdown(
    "Compare the historical IPL performance of two teams."
)


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_head_to_head():

    conn = get_connection()

    query = """
        SELECT
            TEAM1,
            TEAM2,
            MATCHES_PLAYED,
            TEAM1_WINS,
            TEAM2_WINS,
            NO_RESULT_MATCHES,
            TEAM1_WIN_PERCENTAGE,
            TEAM2_WIN_PERCENTAGE
        FROM IPL_ANALYTICS.REPORTING.VW_TEAM_HEAD_TO_HEAD
        ORDER BY MATCHES_PLAYED DESC
    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        "TEAM1",
        "TEAM2",
        "MATCHES_PLAYED",
        "TEAM1_WINS",
        "TEAM2_WINS",
        "NO_RESULT_MATCHES",
        "TEAM1_WIN_PERCENTAGE",
        "TEAM2_WIN_PERCENTAGE"
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

    df = load_head_to_head()

    if df.empty:

        st.warning(
            "No head-to-head data available."
        )

    else:

        # ---------------------------------------------------------------------
        # Numeric Conversion
        # ---------------------------------------------------------------------

        numeric_columns = [
            "MATCHES_PLAYED",
            "TEAM1_WINS",
            "TEAM2_WINS",
            "NO_RESULT_MATCHES",
            "TEAM1_WIN_PERCENTAGE",
            "TEAM2_WIN_PERCENTAGE"
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        # =====================================================================
        # TEAM SELECTION
        # =====================================================================

        st.subheader("🔎 Select Teams")

        teams = sorted(
            set(df["TEAM1"].dropna())
            | set(df["TEAM2"].dropna())
        )

        col1, col2 = st.columns(2)

        with col1:

            team1 = st.selectbox(
                "Team 1",
                teams,
                index=0
            )

        # Try to make Team 2 different from Team 1
        team2_options = [
            team for team in teams
            if team != team1
        ]

        with col2:

            team2 = st.selectbox(
                "Team 2",
                team2_options,
                index=0
            )

        # =====================================================================
        # FIND MATCHUP
        # =====================================================================

        matchup = df[
            (
                (df["TEAM1"] == team1) &
                (df["TEAM2"] == team2)
            )
            |
            (
                (df["TEAM1"] == team2) &
                (df["TEAM2"] == team1)
            )
        ].copy()

        # ---------------------------------------------------------------------
        # Handle matchup not found
        # ---------------------------------------------------------------------

        if matchup.empty:

            st.info(
                f"No head-to-head record found between "
                f"**{team1}** and **{team2}**."
            )

        else:

            row = matchup.iloc[0]

            # -------------------------------------------------------------
            # Normalize team statistics
            # -------------------------------------------------------------

            if row["TEAM1"] == team1:

                team1_wins = int(row["TEAM1_WINS"])
                team2_wins = int(row["TEAM2_WINS"])

                team1_percentage = float(
                    row["TEAM1_WIN_PERCENTAGE"]
                )

                team2_percentage = float(
                    row["TEAM2_WIN_PERCENTAGE"]
                )

            else:

                team1_wins = int(row["TEAM2_WINS"])
                team2_wins = int(row["TEAM1_WINS"])

                team1_percentage = float(
                    row["TEAM2_WIN_PERCENTAGE"]
                )

                team2_percentage = float(
                    row["TEAM1_WIN_PERCENTAGE"]
                )

            matches_played = int(
                row["MATCHES_PLAYED"]
            )

            no_results = int(
                row["NO_RESULT_MATCHES"]
            )

            # =============================================================
            # KPI CARDS
            # =============================================================

            st.divider()

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "🏏 Matches Played",
                    matches_played
                )

            with col2:

                st.metric(
                    f"🏆 {team1} Wins",
                    team1_wins
                )

            with col3:

                st.metric(
                    f"🏆 {team2} Wins",
                    team2_wins
                )

            with col4:

                st.metric(
                    "❌ No Results",
                    no_results
                )

            # =============================================================
            # WIN PERCENTAGE
            # =============================================================

            st.subheader(
                "📊 Win Percentage"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    team1,
                    f"{team1_percentage:.2f}%"
                )

            with col2:

                st.metric(
                    team2,
                    f"{team2_percentage:.2f}%"
                )

            # =============================================================
            # WIN COMPARISON CHART
            # =============================================================

            st.subheader(
                "🏆 Head-to-Head Win Comparison"
            )

            chart_df = pd.DataFrame(
                {
                    "Team": [
                        team1,
                        team2
                    ],
                    "Wins": [
                        team1_wins,
                        team2_wins
                    ]
                }
            )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=chart_df["Team"],
                    y=chart_df["Wins"],
                    text=chart_df["Wins"],
                    textposition="outside"
                )
            )

            fig.update_layout(
                title=f"{team1} vs {team2}",
                xaxis_title="Team",
                yaxis_title="Wins",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # =============================================================
            # WIN PERCENTAGE CHART
            # =============================================================

            percentage_df = pd.DataFrame(
                {
                    "Team": [
                        team1,
                        team2
                    ],
                    "Win Percentage": [
                        team1_percentage,
                        team2_percentage
                    ]
                }
            )

            fig_percentage = go.Figure()

            fig_percentage.add_trace(
                go.Bar(
                    x=percentage_df["Team"],
                    y=percentage_df["Win Percentage"],
                    text=[
                        f"{value:.2f}%"
                        for value in percentage_df[
                            "Win Percentage"
                        ]
                    ],
                    textposition="outside"
                )
            )

            fig_percentage.update_layout(
                title="Win Percentage Comparison",
                xaxis_title="Team",
                yaxis_title="Win Percentage (%)",
                showlegend=False
            )

            st.plotly_chart(
                fig_percentage,
                use_container_width=True
            )

        # =====================================================================
        # ALL HEAD-TO-HEAD MATCHUPS
        # =====================================================================

        st.subheader(
            "📋 Head-to-Head Leaderboard"
        )

        display_df = df.copy()

        display_df = display_df.rename(
            columns={
                "TEAM1": "Team 1",
                "TEAM2": "Team 2",
                "MATCHES_PLAYED": "Matches Played",
                "TEAM1_WINS": "Team 1 Wins",
                "TEAM2_WINS": "Team 2 Wins",
                "NO_RESULT_MATCHES": "No Results",
                "TEAM1_WIN_PERCENTAGE": "Team 1 Win %",
                "TEAM2_WIN_PERCENTAGE": "Team 2 Win %"
            }
        )

        display_df["Team 1 Win %"] = (
            display_df["Team 1 Win %"]
            .round(2)
        )

        display_df["Team 2 Win %"] = (
            display_df["Team 2 Win %"]
            .round(2)
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
        "❌ Unable to load head-to-head data."
    )

    st.code(
        str(e)
    )
