import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection
from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Season Analysis",
    page_icon="📈",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Sidebar Filter
# -----------------------------------------------------------------------------

selected_season = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("📈 Season Analysis")

if selected_season == "All Seasons":
    st.markdown(
        "Explore IPL performance across all seasons."
    )
else:
    st.markdown(
        f"Explore IPL performance for **{selected_season}**."
    )


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_season_data(season):

    conn = get_connection()

    if season == "All Seasons":

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

    else:

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
            WHERE SEASON = %s
            ORDER BY SEASON
        """

        cursor = conn.cursor()

        cursor.execute(query, (season,))

        rows = cursor.fetchall()

        columns = [
            "SEASON",
            "TOTAL_MATCHES",
            "TOTAL_RUNS",
            "TOTAL_WICKETS",
            "AVERAGE_RUNS_PER_MATCH",
            "HIGHEST_MATCH_SCORE",
            "LOWEST_MATCH_SCORE",
            "TOTAL_VENUES",
            "TEAM_OCCURRENCES",
            "UNIQUE_WINNERS"
        ]

        df = pd.DataFrame(rows, columns=columns)

        cursor.close()

    conn.close()

    return df


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

try:

    df = load_season_data(selected_season)

    if df.empty:

        st.warning("No data available for the selected season.")

    else:

        # ---------------------------------------------------------------------
        # KPI Calculations
        # ---------------------------------------------------------------------

        total_matches = int(
            df["TOTAL_MATCHES"].sum()
        )

        total_runs = int(
            df["TOTAL_RUNS"].sum()
        )

        total_wickets = int(
            df["TOTAL_WICKETS"].sum()
        )

        highest_score = int(
            df["HIGHEST_MATCH_SCORE"].max()
        )

        # ---------------------------------------------------------------------
        # KPI Cards
        # ---------------------------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🏏 Total Matches",
                f"{total_matches:,}"
            )

        with col2:
            st.metric(
                "🏃 Total Runs",
                f"{total_runs:,}"
            )

        with col3:
            st.metric(
                "🎯 Total Wickets",
                f"{total_wickets:,}"
            )

        with col4:
            st.metric(
                "🔥 Highest Match Score",
                f"{highest_score:,}"
            )

        st.divider()

        # ---------------------------------------------------------------------
        # All Seasons Charts
        # ---------------------------------------------------------------------

        if selected_season == "All Seasons":

            # -------------------------------------------------------------
            # Matches by Season
            # -------------------------------------------------------------

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

            # -------------------------------------------------------------
            # Runs and Wickets Trend
            # -------------------------------------------------------------

            st.subheader("📊 Runs and Wickets by Season")

            trend_df = df[
                [
                    "SEASON",
                    "TOTAL_RUNS",
                    "TOTAL_WICKETS"
                ]
            ].melt(
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

            # -------------------------------------------------------------
            # Average Runs
            # -------------------------------------------------------------

            st.subheader("🏏 Average Runs per Match")

            fig_average = px.line(
                df,
                x="SEASON",
                y="AVERAGE_RUNS_PER_MATCH",
                markers=True,
                title="Average Runs per Match"
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
        # Selected Season
        # ---------------------------------------------------------------------

        else:

            row = df.iloc[0]

            st.subheader(
                f"📊 {selected_season} Overview"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🏟️ Venues",
                    int(row["TOTAL_VENUES"])
                )

            with col2:
                st.metric(
                    "👥 Team Occurrences",
                    int(row["TEAM_OCCURRENCES"])
                )

            with col3:
                st.metric(
                    "🏆 Unique Winners",
                    int(row["UNIQUE_WINNERS"])
                )

            # -------------------------------------------------------------
            # Season Score Range
            # -------------------------------------------------------------

            score_df = pd.DataFrame({
                "Metric": [
                    "Highest Match Score",
                    "Lowest Match Score"
                ],
                "Score": [
                    int(row["HIGHEST_MATCH_SCORE"]),
                    int(row["LOWEST_MATCH_SCORE"])
                ]
            })

            st.subheader("🔥 Match Score Range")

            fig_score = px.bar(
                score_df,
                x="Metric",
                y="Score",
                text="Score",
                title=f"{selected_season} Match Score Range"
            )

            fig_score.update_traces(
                textposition="outside"
            )

            fig_score.update_layout(
                showlegend=False
            )

            st.plotly_chart(
                fig_score,
                use_container_width=True
            )

        # ---------------------------------------------------------------------
        # Season Statistics Table
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
