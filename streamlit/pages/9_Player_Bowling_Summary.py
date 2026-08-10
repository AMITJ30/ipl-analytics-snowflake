import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection
from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Player Bowling Summary",
    page_icon="🎯",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------------------------

selected_season, selected_team = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🎯 Player Bowling Summary")

st.markdown(
    "Explore overall IPL bowling performance across players."
)


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_bowling_data():

    conn = get_connection()

    query = """
        SELECT
            BOWLER,
            BALLS_BOWLED,
            RUNS_CONCEDED,
            DOT_BALLS,
            WICKETS,
            ECONOMY,
            BOWLING_STRIKE_RATE,
            BOWLING_AVERAGE
        FROM IPL_ANALYTICS.REPORTING.VW_PLAYER_BOWLING_SUMMARY
        ORDER BY WICKETS DESC
    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        "BOWLER",
        "BALLS_BOWLED",
        "RUNS_CONCEDED",
        "DOT_BALLS",
        "WICKETS",
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

    df = load_bowling_data()

    if df.empty:

        st.warning(
            "No bowling summary data available."
        )

    else:

        # ---------------------------------------------------------------------
        # Numeric Conversion
        # ---------------------------------------------------------------------

        numeric_columns = [
            "BALLS_BOWLED",
            "RUNS_CONCEDED",
            "DOT_BALLS",
            "WICKETS",
            "ECONOMY",
            "BOWLING_STRIKE_RATE",
            "BOWLING_AVERAGE"
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        # ---------------------------------------------------------------------
        # Rank Bowlers by Wickets
        # ---------------------------------------------------------------------

        df = (
            df
            .sort_values(
                "WICKETS",
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

        top_bowler = df.iloc[0]

        total_wickets = int(
            df["WICKETS"].sum()
        )

        total_dot_balls = int(
            df["DOT_BALLS"].sum()
        )

        total_runs_conceded = int(
            df["RUNS_CONCEDED"].sum()
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🏆 Top Wicket Taker",
                top_bowler["BOWLER"]
            )

        with col2:

            st.metric(
                "🎯 Top Wickets",
                f"{int(top_bowler['WICKETS']):,}"
            )

        with col3:

            if pd.isna(top_bowler["ECONOMY"]):

                economy_text = "N/A"

            else:

                economy_text = (
                    f"{top_bowler['ECONOMY']:.2f}"
                )

            st.metric(
                "⚡ Economy",
                economy_text
            )

        with col4:

            if pd.isna(top_bowler["BOWLING_AVERAGE"]):

                average_text = "N/A"

            else:

                average_text = (
                    f"{top_bowler['BOWLING_AVERAGE']:.2f}"
                )

            st.metric(
                "📊 Bowling Average",
                average_text
            )

        st.divider()

        # =====================================================================
        # TOP 10 WICKET TAKERS
        # =====================================================================

        st.subheader(
            "🏆 Top 10 Wicket Takers"
        )

        top_10 = (
            df
            .sort_values(
                "WICKETS",
                ascending=False
            )
            .head(10)
            .sort_values(
                "WICKETS"
            )
        )

        fig_wickets = px.bar(
            top_10,
            x="WICKETS",
            y="BOWLER",
            orientation="h",
            text="WICKETS",
            title="Top 10 IPL Wicket Takers"
        )

        fig_wickets.update_traces(
            textposition="outside"
        )

        fig_wickets.update_layout(
            xaxis_title="Wickets",
            yaxis_title="Bowler",
            showlegend=False
        )

        st.plotly_chart(
            fig_wickets,
            use_container_width=True
        )

        # =====================================================================
        # WICKETS VS ECONOMY
        # =====================================================================

        st.subheader(
            "⚡ Wickets vs Economy"
        )

        scatter_df = (
            df
            .dropna(
                subset=[
                    "WICKETS",
                    "ECONOMY"
                ]
            )
            .copy()
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
                "DOT_BALLS",
                "BOWLING_STRIKE_RATE",
                "BOWLING_AVERAGE"
            ],
            title="Wickets vs Economy"
        )

        fig_scatter.update_layout(
            xaxis_title="Wickets",
            yaxis_title="Economy"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

        # =====================================================================
        # TOP DOT BALL BOWLERS
        # =====================================================================

        st.subheader(
            "⚫ Top Dot Ball Bowlers"
        )

        top_dot = (
            df
            .sort_values(
                "DOT_BALLS",
                ascending=False
            )
            .head(10)
            .sort_values(
                "DOT_BALLS"
            )
        )

        fig_dot = px.bar(
            top_dot,
            x="DOT_BALLS",
            y="BOWLER",
            orientation="h",
            text="DOT_BALLS",
            title="Top 10 Dot Ball Bowlers"
        )

        fig_dot.update_traces(
            textposition="outside"
        )

        fig_dot.update_layout(
            xaxis_title="Dot Balls",
            yaxis_title="Bowler",
            showlegend=False
        )

        st.plotly_chart(
            fig_dot,
            use_container_width=True
        )

        # =====================================================================
        # BOWLING LEADERBOARD
        # =====================================================================

        st.subheader(
            "📊 Bowling Leaderboard"
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

        # ---------------------------------------------------------------------
        # Round decimal columns safely
        # ---------------------------------------------------------------------

        display_df["Economy"] = (
            pd.to_numeric(
                display_df["Economy"],
                errors="coerce"
            )
            .round(2)
        )

        display_df["Bowling Strike Rate"] = (
            pd.to_numeric(
                display_df["Bowling Strike Rate"],
                errors="coerce"
            )
            .round(2)
        )

        display_df["Bowling Average"] = (
            pd.to_numeric(
                display_df["Bowling Average"],
                errors="coerce"
            )
            .round(2)
        )

        display_df["Economy"] = (
            display_df["Economy"]
            .fillna("N/A")
        )

        display_df["Bowling Strike Rate"] = (
            display_df["Bowling Strike Rate"]
            .fillna("N/A")
        )

        display_df["Bowling Average"] = (
            display_df["Bowling Average"]
            .fillna("N/A")
        )

        # ---------------------------------------------------------------------
        # Display
        # ---------------------------------------------------------------------

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
        "❌ Unable to load bowling summary."
    )

    st.code(
        str(e)
    )
