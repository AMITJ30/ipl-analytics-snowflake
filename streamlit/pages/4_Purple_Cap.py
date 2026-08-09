import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection
from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Purple Cap",
    page_icon="🎯",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Global Filters
# -----------------------------------------------------------------------------

selected_season, selected_team = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🎯 Purple Cap")

if selected_season == "All Seasons":
    st.markdown(
        "Explore the leading IPL wicket takers across all seasons."
    )
else:
    st.markdown(
        f"Explore the leading wicket takers for **{selected_season}**."
    )


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_purple_cap(season):

    conn = get_connection()

    query = """
        SELECT
            SEASON,
            PLAYER_RANK,
            BOWLER,
            WICKETS,
            BALLS_BOWLED,
            RUNS_CONCEDED,
            DOT_BALLS,
            ECONOMY,
            BOWLING_STRIKE_RATE,
            BOWLING_AVERAGE
        FROM IPL_ANALYTICS.REPORTING.VW_PURPLE_CAP_BY_SEASON
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
        "BOWLER",
        "WICKETS",
        "BALLS_BOWLED",
        "RUNS_CONCEDED",
        "DOT_BALLS",
        "ECONOMY",
        "BOWLING_STRIKE_RATE",
        "BOWLING_AVERAGE"
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

    df = load_purple_cap(selected_season)

    if df.empty:

        st.warning(
            "No Purple Cap data available."
        )

    else:

        # ---------------------------------------------------------------------
        # Numeric conversion
        # ---------------------------------------------------------------------

        numeric_columns = [
            "PLAYER_RANK",
            "WICKETS",
            "BALLS_BOWLED",
            "RUNS_CONCEDED",
            "DOT_BALLS",
            "ECONOMY",
            "BOWLING_STRIKE_RATE",
            "BOWLING_AVERAGE"
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

            top_bowler = df.iloc[0]

            # -----------------------------------------------------------------
            # KPI Cards
            # -----------------------------------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "🏆 Top Wicket Taker",
                    top_bowler["BOWLER"]
                )

            with col2:

                st.metric(
                    "🎯 Wickets",
                    int(top_bowler["WICKETS"])
                )

            with col3:

                if pd.isna(top_bowler["ECONOMY"]):
                    value = "N/A"
                else:
                    value = f"{top_bowler['ECONOMY']:.2f}"

                st.metric(
                    "⚡ Economy",
                    value
                )

            with col4:

                if pd.isna(top_bowler["BOWLING_AVERAGE"]):
                    value = "N/A"
                else:
                    value = f"{top_bowler['BOWLING_AVERAGE']:.2f}"

                st.metric(
                    "📊 Bowling Average",
                    value
                )

            st.divider()

            # -----------------------------------------------------------------
            # Top 10 Wicket Takers
            # -----------------------------------------------------------------

            st.subheader(
                f"🏆 Top 10 Wicket Takers — {selected_season}"
            )

            top_10 = (
                df
                .sort_values("PLAYER_RANK")
                .head(10)
                .sort_values("WICKETS")
            )

            fig = px.bar(
                top_10,
                x="WICKETS",
                y="BOWLER",
                orientation="h",
                text="WICKETS",
                title=f"Top 10 Wicket Takers — {selected_season}"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                xaxis_title="Wickets",
                yaxis_title="Bowler",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # -----------------------------------------------------------------
            # Economy vs Wickets
            # -----------------------------------------------------------------

            st.subheader(
                "⚡ Economy vs Wickets"
            )

            scatter_df = df.head(50).copy()

            scatter_df = scatter_df.dropna(
                subset=[
                    "WICKETS",
                    "ECONOMY"
                ]
            )

            fig_scatter = px.scatter(
                scatter_df,
                x="WICKETS",
                y="ECONOMY",
                size="DOT_BALLS",
                hover_name="BOWLER",
                hover_data=[
                    "BALLS_BOWLED",
                    "RUNS_CONCEDED",
                    "BOWLING_STRIKE_RATE",
                    "BOWLING_AVERAGE"
                ],
                title=f"Wickets vs Economy — {selected_season}"
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
                "🏆 Season-wise Purple Cap Leaders"
            )

            # -----------------------------------------------------------------
            # Get #1 bowler from every season
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
                y="WICKETS",
                text="WICKETS",
                hover_name="BOWLER",
                title="Purple Cap Leader by Season"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                xaxis_title="Season",
                yaxis_title="Wickets",
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
            "📊 Purple Cap Leaderboard"
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
                "BOWLER": "Bowler",
                "WICKETS": "Wickets",
                "BALLS_BOWLED": "Balls Bowled",
                "RUNS_CONCEDED": "Runs Conceded",
                "DOT_BALLS": "Dot Balls",
                "ECONOMY": "Economy",
                "BOWLING_STRIKE_RATE": "Bowling Strike Rate",
                "BOWLING_AVERAGE": "Bowling Average"
            }
        )

        display_df["Economy"] = (
            display_df["Economy"]
            .round(2)
        )

        display_df["Bowling Strike Rate"] = (
            display_df["Bowling Strike Rate"]
            .round(2)
        )

        display_df["Bowling Average"] = (
            display_df["Bowling Average"]
            .round(2)
        )

        display_df["Bowling Strike Rate"] = (
            display_df["Bowling Strike Rate"]
            .fillna("N/A")
        )

        display_df["Bowling Average"] = (
            display_df["Bowling Average"]
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
        "❌ Unable to load Purple Cap data."
    )

    st.code(
        str(e)
    )
