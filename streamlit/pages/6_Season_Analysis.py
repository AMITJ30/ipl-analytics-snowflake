import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Season Analysis",
    page_icon="📈",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("📈 Season Analysis")

st.markdown(
    "Explore how IPL seasons have evolved across matches, runs, wickets and venues."
)


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_season_data():

    conn = get_connection()

    query = """
        SELECT
            SEASON,
            TOTAL_MATCHES,
            TOTAL_RUNS,
            TOTAL_WICKETS,
            AVERAGE_RUNS_PER_MATCH,
            HIGHEST_MATCH_SCORE,
            LOWEST_MATCH_SCORE,
            TOTAL_VENUES,
            TEAM_OCCURRENCES,
            UNIQUE_WINNERS
        FROM REPORTING.VW_SEASON_SUMMARY
        ORDER BY SEASON
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

try:

    df = load_season_data()

    if df.empty:

        st.warning("No season data available.")

    else:

        # ---------------------------------------------------------------------
        # KPI Calculations
        # ---------------------------------------------------------------------

        total_seasons = len(df)

        highest_scoring_season = df.loc[
            df["TOTAL_RUNS"].idxmax(),
            "SEASON"
        ]

        highest_match_score = df["HIGHEST_MATCH_SCORE"].max()

        most_matches_season = df.loc[
            df["TOTAL_MATCHES"].idxmax(),
            "SEASON"
        ]

        # ---------------------------------------------------------------------
        # KPI Cards
        # ---------------------------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📅 Seasons",
                total_seasons
            )

        with col2:
            st.metric(
                "🏏 Highest Run-Scoring Season",
                highest_scoring_season
            )

        with col3:
            st.metric(
                "🔥 Highest Match Score",
                f"{int(highest_match_score):,}"
            )

        with col4:
            st.metric(
                "🏆 Most Matches Season",
                most_matches_season
            )

        st.divider()

        # ---------------------------------------------------------------------
        # Matches by Season
        # ---------------------------------------------------------------------

        st.subheader("🏏 Matches Played by Season")

        fig_matches = px.bar(
            df,
            x="SEASON",
            y="TOTAL_MATCHES",
            text="TOTAL_MATCHES",
            title="IPL Matches by Season"
        )

        fig_matches.update_traces(
            textposition="outside"
        )

        fig_matches.update_layout(
            xaxis_title="Season",
            yaxis_title="Matches",
            showlegend=False
        )

        st.plotly_chart(
            fig_matches,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Runs and Wickets Trend
        # ---------------------------------------------------------------------

        st.subheader("📊 Runs and Wickets by Season")

        trend_df = df[
            [
                "SEASON",
                "TOTAL_RUNS",
                "TOTAL_WICKETS"
            ]
        ].copy()

        trend_df = trend_df.melt(
            id_vars="SEASON",
            var_name="Metric",
            value_name="Value"
        )

        fig_trend = px.line(
            trend_df,
            x="SEASON",
            y="Value",
            color="Metric",
            markers=True,
            title="Runs and Wickets Trend"
        )

        fig_trend.update_layout(
            xaxis_title="Season",
            yaxis_title="Count"
        )

        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Average Runs per Match
        # ---------------------------------------------------------------------

        st.subheader("🏏 Average Runs per Match")

        fig_average = px.line(
            df,
            x="SEASON",
            y="AVERAGE_RUNS_PER_MATCH",
            markers=True,
            title="Average Runs per Match by Season"
        )

        fig_average.update_layout(
            xaxis_title="Season",
            yaxis_title="Average Runs"
        )

        st.plotly_chart(
            fig_average,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Highest Match Score
        # ---------------------------------------------------------------------

        st.subheader("🔥 Highest Match Score by Season")

        fig_highest = px.bar(
            df,
            x="SEASON",
            y="HIGHEST_MATCH_SCORE",
            text="HIGHEST_MATCH_SCORE",
            title="Highest Match Score by Season"
        )

        fig_highest.update_traces(
            textposition="outside"
        )

        fig_highest.update_layout(
            xaxis_title="Season",
            yaxis_title="Highest Match Score",
            showlegend=False
        )

        st.plotly_chart(
            fig_highest,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Detailed Table
        # ---------------------------------------------------------------------

        st.subheader("📋 Season Statistics")

        display_df = df.copy()

        display_df = display_df.rename(
            columns={
                "SEASON": "Season",
                "TOTAL_MATCHES": "Total Matches",
                "TOTAL_RUNS": "Total Runs",
                "TOTAL_WICKETS": "Total Wickets",
                "AVERAGE_RUNS_PER_MATCH": "Average Runs / Match",
                "HIGHEST_MATCH_SCORE": "Highest Match Score",
                "LOWEST_MATCH_SCORE": "Lowest Match Score",
                "TOTAL_VENUES": "Total Venues",
                "TEAM_OCCURRENCES": "Team Occurrences",
                "UNIQUE_WINNERS": "Unique Winners"
            }
        )

        display_df["Average Runs / Match"] = (
            display_df["Average Runs / Match"].round(2)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


except Exception as e:

    st.error("❌ Unable to load season analytics.")

    st.code(str(e))
