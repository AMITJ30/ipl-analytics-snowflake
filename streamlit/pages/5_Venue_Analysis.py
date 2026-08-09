import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Venue Analysis",
    page_icon="🏟️",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🏟️ Venue Analysis")

st.markdown(
    "Analyze IPL venues based on matches, scoring and wicket patterns."
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
        FROM REPORTING.VW_VENUE_ANALYTICS
        ORDER BY MATCHES_PLAYED DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

try:

    df = load_venue_data()

    if df.empty:

        st.warning("No venue data available.")

    else:

        # ---------------------------------------------------------------------
        # KPI Calculations
        # ---------------------------------------------------------------------

        total_venues = len(df)

        most_used_venue = df.iloc[0]["VENUE"]

        highest_score = df["HIGHEST_MATCH_SCORE"].max()

        highest_score_venue = df.loc[
            df["HIGHEST_MATCH_SCORE"].idxmax(),
            "VENUE"
        ]

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
                "🏏 Most Used Venue",
                most_used_venue
            )

        with col3:
            st.metric(
                "🔥 Highest Match Score",
                f"{int(highest_score):,}"
            )

        with col4:
            st.metric(
                "📍 Highest Score Venue",
                highest_score_venue
            )

        st.divider()

        # ---------------------------------------------------------------------
        # Matches Played by Venue
        # ---------------------------------------------------------------------

        st.subheader("🏟️ Matches Played by Venue")

        top_venues = df.sort_values(
            "MATCHES_PLAYED",
            ascending=False
        ).head(15)

        fig = px.bar(
            top_venues.sort_values("MATCHES_PLAYED"),
            x="MATCHES_PLAYED",
            y="VENUE",
            orientation="h",
            text="MATCHES_PLAYED",
            title="Top 15 Venues by Matches Played"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Matches Played",
            yaxis_title="Venue",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Average Runs per Match
        # ---------------------------------------------------------------------

        st.subheader("🏏 Average Runs per Match")

        scoring_venues = df.sort_values(
            "AVERAGE_RUNS_PER_MATCH",
            ascending=False
        ).head(15)

        fig_runs = px.bar(
            scoring_venues.sort_values(
                "AVERAGE_RUNS_PER_MATCH"
            ),
            x="AVERAGE_RUNS_PER_MATCH",
            y="VENUE",
            orientation="h",
            text="AVERAGE_RUNS_PER_MATCH",
            title="Top 15 High-Scoring Venues"
        )

        fig_runs.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside"
        )

        fig_runs.update_layout(
            xaxis_title="Average Runs per Match",
            yaxis_title="Venue",
            showlegend=False
        )

        st.plotly_chart(
            fig_runs,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Highest vs Lowest Score
        # ---------------------------------------------------------------------

        st.subheader("🔥 Highest vs Lowest Match Score")

        score_df = df.sort_values(
            "HIGHEST_MATCH_SCORE",
            ascending=False
        ).head(15)

        fig_scores = px.bar(
            score_df,
            x="VENUE",
            y=[
                "HIGHEST_MATCH_SCORE",
                "LOWEST_MATCH_SCORE"
            ],
            barmode="group",
            title="Highest and Lowest Match Scores"
        )

        fig_scores.update_layout(
            xaxis_title="Venue",
            yaxis_title="Score"
        )

        st.plotly_chart(
            fig_scores,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Detailed Table
        # ---------------------------------------------------------------------

        st.subheader("📊 Venue Statistics")

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
            display_df["Average Runs / Match"].round(2)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


except Exception as e:

    st.error("❌ Unable to load venue analytics.")

    st.code(str(e))
