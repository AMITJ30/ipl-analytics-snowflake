import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.connection import get_connection


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Team Head-to-Head",
    page_icon="⚔️",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("⚔️ Team Head-to-Head")

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
        FROM REPORTING.VW_TEAM_HEAD_TO_HEAD
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

try:

    df = load_head_to_head()

    if df.empty:

        st.warning("No head-to-head data available.")

    else:

        # ---------------------------------------------------------------------
        # Team Selection
        # ---------------------------------------------------------------------

        teams = sorted(
            set(df["TEAM1"].dropna()) |
            set(df["TEAM2"].dropna())
        )

        col1, col2 = st.columns(2)

        with col1:
            team1 = st.selectbox(
                "Select Team 1",
                teams
            )

        with col2:
            team2_options = [
                team for team in teams
                if team != team1
            ]

            team2 = st.selectbox(
                "Select Team 2",
                team2_options
            )

        # ---------------------------------------------------------------------
        # Find Matchup
        # ---------------------------------------------------------------------

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
        ]

        if matchup.empty:

            st.warning(
                f"No head-to-head data found for {team1} vs {team2}."
            )

        else:

            row = matchup.iloc[0]

            # -----------------------------------------------------------------
            # Normalize Team Statistics
            # -----------------------------------------------------------------

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

            matches_played = int(row["MATCHES_PLAYED"])

            no_results = int(row["NO_RESULT_MATCHES"])

            # -----------------------------------------------------------------
            # KPI Cards
            # -----------------------------------------------------------------

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
                    "➖ No Results",
                    no_results
                )

            # -----------------------------------------------------------------
            # Win Percentage
            # -----------------------------------------------------------------

            st.subheader("📊 Win Percentage")

            fig_percentage = go.Figure()

            fig_percentage.add_trace(
                go.Bar(
                    x=[team1],
                    y=[team1_percentage],
                    text=[f"{team1_percentage:.2f}%"],
                    textposition="auto",
                    name=team1
                )
            )

            fig_percentage.add_trace(
                go.Bar(
                    x=[team2],
                    y=[team2_percentage],
                    text=[f"{team2_percentage:.2f}%"],
                    textposition="auto",
                    name=team2
                )
            )

            fig_percentage.update_layout(
                yaxis_title="Win Percentage (%)",
                yaxis=dict(range=[0, 100]),
                showlegend=False
            )

            st.plotly_chart(
                fig_percentage,
                use_container_width=True
            )

            # -----------------------------------------------------------------
            # Wins Comparison
            # -----------------------------------------------------------------

            st.subheader("🏆 Wins Comparison")

            fig_wins = go.Figure()

            fig_wins.add_trace(
                go.Bar(
                    x=[team1],
                    y=[team1_wins],
                    text=[team1_wins],
                    textposition="auto",
                    name=team1
                )
            )

            fig_wins.add_trace(
                go.Bar(
                    x=[team2],
                    y=[team2_wins],
                    text=[team2_wins],
                    textposition="auto",
                    name=team2
                )
            )

            fig_wins.update_layout(
                yaxis_title="Matches Won",
                showlegend=False
            )

            st.plotly_chart(
                fig_wins,
                use_container_width=True
            )

            # -----------------------------------------------------------------
            # Summary
            # -----------------------------------------------------------------

            st.subheader("📋 Head-to-Head Summary")

            summary_df = pd.DataFrame({
                "Team": [
                    team1,
                    team2
                ],
                "Wins": [
                    team1_wins,
                    team2_wins
                ],
                "Win Percentage": [
                    team1_percentage,
                    team2_percentage
                ]
            })

            summary_df["Win Percentage"] = (
                summary_df["Win Percentage"].round(2)
            )

            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True
            )


except Exception as e:

    st.error("❌ Unable to load head-to-head data.")

    st.code(str(e))
