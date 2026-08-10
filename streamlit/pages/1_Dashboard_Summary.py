import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection
from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Dashboard Summary",
    page_icon="📊",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------------------------

selected_season, selected_team = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("📊 IPL Dashboard Summary")

if selected_season == "All Seasons":
    st.markdown(
        "Get a high-level overview of IPL statistics across all seasons."
    )
else:
    st.markdown(
        f"Get a high-level overview of **{selected_season}**."
    )


# -----------------------------------------------------------------------------
# Load Dashboard Summary
# -----------------------------------------------------------------------------

@st.cache_data
def load_dashboard_summary():

    conn = get_connection()

    query = """
        SELECT
            TOTAL_MATCHES,
            TOTAL_SEASONS,
            TOTAL_TEAMS,
            TOTAL_PLAYERS,
            TOTAL_VENUES,
            TOTAL_DELIVERIES,
            TOTAL_RUNS,
            TOTAL_WICKETS,
            HIGHEST_MATCH_SCORE,
            LOWEST_MATCH_SCORE,
            AVERAGE_MATCH_SCORE
        FROM IPL_ANALYTICS.REPORTING.VW_DASHBOARD_SUMMARY
    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        "TOTAL_MATCHES",
        "TOTAL_SEASONS",
        "TOTAL_TEAMS",
        "TOTAL_PLAYERS",
        "TOTAL_VENUES",
        "TOTAL_DELIVERIES",
        "TOTAL_RUNS",
        "TOTAL_WICKETS",
        "HIGHEST_MATCH_SCORE",
        "LOWEST_MATCH_SCORE",
        "AVERAGE_MATCH_SCORE"
    ]

    df = pd.DataFrame(
        rows,
        columns=columns
    )

    cursor.close()
    conn.close()

    return df


# -----------------------------------------------------------------------------
# Load Season Data for Charts
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
            LOWEST_MATCH_SCORE
        FROM IPL_ANALYTICS.REPORTING.VW_SEASON_SUMMARY
        ORDER BY SEASON
    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        "SEASON",
        "TOTAL_MATCHES",
        "TOTAL_RUNS",
        "TOTAL_WICKETS",
        "AVERAGE_RUNS_PER_MATCH",
        "HIGHEST_MATCH_SCORE",
        "LOWEST_MATCH_SCORE"
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

    summary_df = load_dashboard_summary()

    if summary_df.empty:

        st.warning(
            "No dashboard summary data available."
        )

    else:

        # ---------------------------------------------------------------------
        # Get Summary Row
        # ---------------------------------------------------------------------

        summary = summary_df.iloc[0]

        # ---------------------------------------------------------------------
        # Numeric Conversion
        # ---------------------------------------------------------------------

        numeric_columns = [
            "TOTAL_MATCHES",
            "TOTAL_SEASONS",
            "TOTAL_TEAMS",
            "TOTAL_PLAYERS",
            "TOTAL_VENUES",
            "TOTAL_DELIVERIES",
            "TOTAL_RUNS",
            "TOTAL_WICKETS",
            "HIGHEST_MATCH_SCORE",
            "LOWEST_MATCH_SCORE",
            "AVERAGE_MATCH_SCORE"
        ]

        for column in numeric_columns:

            summary_df[column] = pd.to_numeric(
                summary_df[column],
                errors="coerce"
            )

        summary = summary_df.iloc[0]

        # =====================================================================
        # KPI SECTION
        # =====================================================================

        st.subheader("📌 IPL Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🏏 Total Matches",
                f"{int(summary['TOTAL_MATCHES']):,}"
            )

        with col2:

            st.metric(
                "📅 Total Seasons",
                int(summary["TOTAL_SEASONS"])
            )

        with col3:

            st.metric(
                "👥 Total Teams",
                int(summary["TOTAL_TEAMS"])
            )

        with col4:

            st.metric(
                "🏃 Total Players",
                f"{int(summary['TOTAL_PLAYERS']):,}"
            )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🏟️ Total Venues",
                int(summary["TOTAL_VENUES"])
            )

        with col2:

            st.metric(
                "🏏 Total Deliveries",
                f"{int(summary['TOTAL_DELIVERIES']):,}"
            )

        with col3:

            st.metric(
                "🏃 Total Runs",
                f"{int(summary['TOTAL_RUNS']):,}"
            )

        with col4:

            st.metric(
                "🎯 Total Wickets",
                f"{int(summary['TOTAL_WICKETS']):,}"
            )

        st.divider()

        # =====================================================================
        # SCORE SUMMARY
        # =====================================================================

        st.subheader("🔥 Match Score Summary")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🔥 Highest Match Score",
                int(summary["HIGHEST_MATCH_SCORE"])
            )

        with col2:

            st.metric(
                "📉 Lowest Match Score",
                int(summary["LOWEST_MATCH_SCORE"])
            )

        with col3:

            st.metric(
                "📊 Average Match Score",
                f"{summary['AVERAGE_MATCH_SCORE']:.2f}"
            )

        st.divider()

        # =====================================================================
        # SEASON DATA
        # =====================================================================

        season_df = load_season_data()

        if not season_df.empty:

            # -------------------------------------------------------------
            # Numeric Conversion
            # -------------------------------------------------------------

            season_numeric_columns = [
                "TOTAL_MATCHES",
                "TOTAL_RUNS",
                "TOTAL_WICKETS",
                "AVERAGE_RUNS_PER_MATCH",
                "HIGHEST_MATCH_SCORE",
                "LOWEST_MATCH_SCORE"
            ]

            for column in season_numeric_columns:

                season_df[column] = pd.to_numeric(
                    season_df[column],
                    errors="coerce"
                )

            # -------------------------------------------------------------
            # Season order
            # -------------------------------------------------------------

            season_order = [
                "IPL-2008",
                "IPL-2009",
                "IPL-2010",
                "IPL-2011",
                "IPL-2012",
                "IPL-2013",
                "IPL-2014",
                "IPL-2015",
                "IPL-2016",
                "IPL-2017",
                "IPL-2018",
                "IPL-2019"
            ]

            season_df["SEASON"] = pd.Categorical(
                season_df["SEASON"],
                categories=season_order,
                ordered=True
            )

            season_df = season_df.sort_values(
                "SEASON"
            )

            # =============================================================
            # MATCHES BY SEASON
            # =============================================================

            st.subheader(
                "🏏 Matches by Season"
            )

            fig_matches = px.bar(
                season_df,
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

            # =============================================================
            # RUNS BY SEASON
            # =============================================================

            st.subheader(
                "🏃 Runs by Season"
            )

            fig_runs = px.line(
                season_df,
                x="SEASON",
                y="TOTAL_RUNS",
                markers=True,
                title="Total Runs by Season"
            )

            fig_runs.update_layout(
                xaxis_title="Season",
                yaxis_title="Total Runs"
            )

            st.plotly_chart(
                fig_runs,
                use_container_width=True
            )

            # =============================================================
            # WICKETS BY SEASON
            # =============================================================

            st.subheader(
                "🎯 Wickets by Season"
            )

            fig_wickets = px.line(
                season_df,
                x="SEASON",
                y="TOTAL_WICKETS",
                markers=True,
                title="Total Wickets by Season"
            )

            fig_wickets.update_layout(
                xaxis_title="Season",
                yaxis_title="Total Wickets"
            )

            st.plotly_chart(
                fig_wickets,
                use_container_width=True
            )

            # =============================================================
            # AVERAGE RUNS BY SEASON
            # =============================================================

            st.subheader(
                "📈 Average Runs per Match"
            )

            fig_average = px.line(
                season_df,
                x="SEASON",
                y="AVERAGE_RUNS_PER_MATCH",
                markers=True,
                title="Average Runs per Match by Season"
            )

            fig_average.update_layout(
                xaxis_title="Season",
                yaxis_title="Average Runs per Match"
            )

            st.plotly_chart(
                fig_average,
                use_container_width=True
            )

        # =====================================================================
        # DATA SUMMARY TABLE
        # =====================================================================

        st.subheader(
            "📋 IPL Summary"
        )

        display_df = summary_df.copy()

        display_df = display_df.rename(
            columns={
                "TOTAL_MATCHES": "Total Matches",
                "TOTAL_SEASONS": "Total Seasons",
                "TOTAL_TEAMS": "Total Teams",
                "TOTAL_PLAYERS": "Total Players",
                "TOTAL_VENUES": "Total Venues",
                "TOTAL_DELIVERIES": "Total Deliveries",
                "TOTAL_RUNS": "Total Runs",
                "TOTAL_WICKETS": "Total Wickets",
                "HIGHEST_MATCH_SCORE": "Highest Match Score",
                "LOWEST_MATCH_SCORE": "Lowest Match Score",
                "AVERAGE_MATCH_SCORE": "Average Match Score"
            }
        )

        display_df["Average Match Score"] = (
            display_df["Average Match Score"]
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
        "❌ Unable to load dashboard summary."
    )

    st.code(
        str(e)
    )
