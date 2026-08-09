import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection
from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Venue Analytics",
    page_icon="🏟️",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Global Filters
# -----------------------------------------------------------------------------

selected_season, selected_team = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🏟️ Venue Analytics")

st.markdown(
    "Analyze IPL performance across different venues."
)


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_venue_data():

    conn = get_connection()

    query = """
        SELECT
            VENUE,
            MATCHES_PLAYED,
            TOTAL_RUNS,
            TOTAL_WICKETS,
            AVERAGE_RUNS_PER_MATCH,
            HIGHEST_MATCH_SCORE,
            LOWEST_MATCH_SCORE
        FROM IPL_ANALYTICS.REPORTING.VW_VENUE_ANALYTICS
        ORDER BY MATCHES_PLAYED DESC
    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        "VENUE",
        "MATCHES_PLAYED",
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

    df = load_venue_data()

    if df.empty:

        st.warning(
            "No venue analytics data available."
        )

    else:

        # ---------------------------------------------------------------------
        # Numeric conversion
        # ---------------------------------------------------------------------

        numeric_columns = [
            "MATCHES_PLAYED",
            "TOTAL_RUNS",
            "TOTAL_WICKETS",
            "AVERAGE_RUNS_PER_MATCH",
            "HIGHEST_MATCH_SCORE",
            "LOWEST_MATCH_SCORE"
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        # ---------------------------------------------------------------------
        # Top venue
        # ---------------------------------------------------------------------

        top_venue = (
            df
            .sort_values(
                "MATCHES_PLAYED",
                ascending=False
            )
            .iloc[0]
        )

        # ---------------------------------------------------------------------
        # Overall KPIs
        # ---------------------------------------------------------------------

        total_venues = len(df)

        total_matches = int(
            df["MATCHES_PLAYED"].sum()
        )

        total_runs = int(
            df["TOTAL_RUNS"].sum()
        )

        total_wickets = int(
            df["TOTAL_WICKETS"].sum()
        )

        # ---------------------------------------------------------------------
        # KPI Cards
        # ---------------------------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🏟️ Total Venues",
                total_venues
            )

        with col2:

            st.metric(
                "🏏 Total Matches",
                f"{total_matches:,}"
            )

        with col3:

            st.metric(
                "🏃 Total Runs",
                f"{total_runs:,}"
            )

        with col4:

            st.metric(
                "🎯 Total Wickets",
                f"{total_wickets:,}"
            )

        st.divider()

        # ---------------------------------------------------------------------
        # Top Venues by Matches
        # ---------------------------------------------------------------------

        st.subheader(
            "🏟️ Top Venues by Matches Played"
        )

        top_venues = (
            df
            .sort_values(
                "MATCHES_PLAYED",
                ascending=False
            )
            .head(10)
            .sort_values(
                "MATCHES_PLAYED"
            )
        )

        fig_matches = px.bar(
            top_venues,
            x="MATCHES_PLAYED",
            y="VENUE",
            orientation="h",
            text="MATCHES_PLAYED",
            title="Top 10 Venues by Matches Played"
        )

        fig_matches.update_traces(
            textposition="outside"
        )

        fig_matches.update_layout(
            xaxis_title="Matches Played",
            yaxis_title="Venue",
            showlegend=False
        )

        st.plotly_chart(
            fig_matches,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Average Runs per Match
        # ---------------------------------------------------------------------

        st.subheader(
            "🏏 Average Runs per Match"
        )

        average_df = (
            df
            .sort_values(
                "AVERAGE_RUNS_PER_MATCH",
                ascending=False
            )
            .head(10)
            .sort_values(
                "AVERAGE_RUNS_PER_MATCH"
            )
        )

        fig_average = px.bar(
            average_df,
            x="AVERAGE_RUNS_PER_MATCH",
            y="VENUE",
            orientation="h",
            text="AVERAGE_RUNS_PER_MATCH",
            title="Top 10 High-Scoring Venues"
        )

        fig_average.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig_average.update_layout(
            xaxis_title="Average Runs per Match",
            yaxis_title="Venue",
            showlegend=False
        )

        st.plotly_chart(
            fig_average,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Runs vs Wickets
        # ---------------------------------------------------------------------

        st.subheader(
            "📊 Runs vs Wickets by Venue"
        )

        scatter_df = df.dropna(
            subset=[
                "TOTAL_RUNS",
                "TOTAL_WICKETS"
            ]
        )

        fig_scatter = px.scatter(
            scatter_df,
            x="TOTAL_RUNS",
            y="TOTAL_WICKETS",
            size="MATCHES_PLAYED",
            hover_name="VENUE",
            hover_data=[
                "AVERAGE_RUNS_PER_MATCH",
                "HIGHEST_MATCH_SCORE",
                "LOWEST_MATCH_SCORE"
            ],
            title="Total Runs vs Total Wickets"
        )

        fig_scatter.update_layout(
            xaxis_title="Total Runs",
            yaxis_title="Total Wickets"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Venue Leaderboard
        # ---------------------------------------------------------------------

        st.subheader(
            "📋 Venue Leaderboard"
        )

        display_df = df.copy()

        display_df = display_df.rename(
            columns={
                "VENUE": "Venue",
                "MATCHES_PLAYED": "Matches Played",
                "TOTAL_RUNS": "Total Runs",
                "TOTAL_WICKETS": "Total Wickets",
                "AVERAGE_RUNS_PER_MATCH": "Average Runs / Match",
                "HIGHEST_MATCH_SCORE": "Highest Match Score",
                "LOWEST_MATCH_SCORE": "Lowest Match Score"
            }
        )

        display_df["Average Runs / Match"] = (
            display_df["Average Runs / Match"]
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
        "❌ Unable to load venue analytics."
    )

    st.code(
        str(e)
    )
