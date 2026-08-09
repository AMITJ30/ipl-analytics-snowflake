import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection
from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Orange Cap",
    page_icon="🏏",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Global Filters
# -----------------------------------------------------------------------------

selected_season, selected_team = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🏏 Orange Cap")

if selected_season == "All Seasons":
    st.markdown(
        "Explore the leading IPL run scorers across all seasons."
    )
else:
    st.markdown(
        f"Explore the leading run scorers for **{selected_season}**."
    )


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_orange_cap(season):

    conn = get_connection()

    query = """
        SELECT
            SEASON,
            PLAYER_RANK,
            BATSMAN,
            TOTAL_RUNS,
            BALLS_FACED,
            FOURS,
            SIXES,
            STRIKE_RATE,
            BATTING_AVERAGE
        FROM IPL_ANALYTICS.REPORTING.VW_ORANGE_CAP_BY_SEASON
    """

    params = ()

    if season != "All Seasons":
        query += """
            WHERE SEASON = %s
        """
        params = (season,)

    query += """
        ORDER BY SEASON, PLAYER_RANK
    """

    cursor = conn.cursor()
    cursor.execute(query, params)

    rows = cursor.fetchall()

    columns = [
        "SEASON",
        "PLAYER_RANK",
        "BATSMAN",
        "TOTAL_RUNS",
        "BALLS_FACED",
        "FOURS",
        "SIXES",
        "STRIKE_RATE",
        "BATTING_AVERAGE"
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

    df = load_orange_cap(selected_season)

    if df.empty:

        st.warning("No Orange Cap data available.")

    else:

        # ---------------------------------------------------------------------
        # Numeric conversion
        # ---------------------------------------------------------------------

        numeric_columns = [
            "PLAYER_RANK",
            "TOTAL_RUNS",
            "BALLS_FACED",
            "FOURS",
            "SIXES",
            "STRIKE_RATE",
            "BATTING_AVERAGE"
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        # =====================================================================
        # SPECIFIC SEASON
        # =====================================================================

        if selected_season != "All Seasons":

            df = df.sort_values(
                "PLAYER_RANK"
            )

            top_player = df.iloc[0]

            # -----------------------------------------------------------------
            # KPI Cards
            # -----------------------------------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "🏆 Top Run Scorer",
                    top_player["BATSMAN"]
                )

            with col2:

                st.metric(
                    "🏏 Total Runs",
                    f"{int(top_player['TOTAL_RUNS']):,}"
                )

            with col3:

                if pd.isna(top_player["STRIKE_RATE"]):
                    value = "N/A"
                else:
                    value = f"{top_player['STRIKE_RATE']:.2f}"

                st.metric(
                    "⚡ Strike Rate",
                    value
                )

            with col4:

                if pd.isna(top_player["BATTING_AVERAGE"]):
                    value = "N/A"
                else:
                    value = f"{top_player['BATTING_AVERAGE']:.2f}"

                st.metric(
                    "📊 Batting Average",
                    value
                )

            st.divider()

            # -----------------------------------------------------------------
            # Top 10 Run Scorers
            # -----------------------------------------------------------------

            st.subheader(
                f"🏆 Top 10 Run Scorers — {selected_season}"
            )

            top_10 = (
                df
                .sort_values("PLAYER_RANK")
                .head(10)
                .sort_values("TOTAL_RUNS")
            )

            fig = px.bar(
                top_10,
                x="TOTAL_RUNS",
                y="BATSMAN",
                orientation="h",
                text="TOTAL_RUNS",
                title=f"Top 10 Run Scorers — {selected_season}"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                xaxis_title="Total Runs",
                yaxis_title="Batsman",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # -----------------------------------------------------------------
            # Strike Rate vs Runs
            # -----------------------------------------------------------------

            st.subheader(
                "⚡ Strike Rate vs Total Runs"
            )

            scatter_df = df.head(50).copy()

            scatter_df = scatter_df.dropna(
                subset=[
                    "TOTAL_RUNS",
                    "STRIKE_RATE"
                ]
            )

            fig_scatter = px.scatter(
                scatter_df,
                x="TOTAL_RUNS",
                y="STRIKE_RATE",
                size="SIXES",
                hover_name="BATSMAN",
                hover_data=[
                    "BALLS_FACED",
                    "FOURS",
                    "SIXES",
                    "BATTING_AVERAGE"
                ],
                title=f"Runs vs Strike Rate — {selected_season}"
            )

            st.plotly_chart(
                fig_scatter,
                use_container_width=True
            )

        # =====================================================================
        # ALL SEASONS
        # =====================================================================

        else:

            st.subheader(
                "🏆 Season-wise Orange Cap Leaders"
            )

            # -----------------------------------------------------------------
            # Get #1 player from every season
            # -----------------------------------------------------------------

            leaders = (
                df[
                    df["PLAYER_RANK"] == 1
                ]
                .sort_values("SEASON")
                .copy()
            )

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

            leaders["SEASON"] = pd.Categorical(
                leaders["SEASON"],
                categories=season_order,
                ordered=True
            )

            leaders = leaders.sort_values(
                "SEASON"
            )

            fig = px.bar(
                leaders,
                x="SEASON",
                y="TOTAL_RUNS",
                text="TOTAL_RUNS",
                hover_name="BATSMAN",
                title="Orange Cap Leader by Season"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                xaxis_title="Season",
                yaxis_title="Total Runs",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =====================================================================
        # LEADERBOARD
        # =====================================================================

        st.subheader(
            "📊 Orange Cap Leaderboard"
        )

        if selected_season == "All Seasons":

            # Top 10 from EVERY season
            display_df = (
                df[
                    df["PLAYER_RANK"] <= 10
                ]
                .sort_values(
                    ["SEASON", "PLAYER_RANK"]
                )
                .copy()
            )

        else:

            # Top 10 from selected season
            display_df = (
                df
                .sort_values("PLAYER_RANK")
                .head(10)
                .copy()
            )

        display_df = display_df.rename(
            columns={
                "SEASON": "Season",
                "PLAYER_RANK": "Rank",
                "BATSMAN": "Batsman",
                "TOTAL_RUNS": "Total Runs",
                "BALLS_FACED": "Balls Faced",
                "FOURS": "Fours",
                "SIXES": "Sixes",
                "STRIKE_RATE": "Strike Rate",
                "BATTING_AVERAGE": "Batting Average"
            }
        )

        display_df["Strike Rate"] = (
            display_df["Strike Rate"]
            .round(2)
        )

        display_df["Batting Average"] = (
            display_df["Batting Average"]
            .round(2)
        )

        display_df["Batting Average"] = (
            display_df["Batting Average"]
            .fillna("N/A")
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
        "❌ Unable to load Orange Cap data."
    )

    st.code(
        str(e)
    )
