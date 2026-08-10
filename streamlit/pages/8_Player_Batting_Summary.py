import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection
from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Player Batting Summary",
    page_icon="🏏",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------------------------

selected_season, selected_team = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🏏 Player Batting Summary")

st.markdown(
    "Explore overall IPL batting performance across players."
)


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_batting_data():

    conn = get_connection()

    query = """
        SELECT
            PLAYER_RANK,
            BATSMAN,
            TOTAL_RUNS,
            BALLS_FACED,
            FOURS,
            SIXES,
            STRIKE_RATE,
            BATTING_AVERAGE
        FROM IPL_ANALYTICS.REPORTING.VW_PLAYER_BATTING_SUMMARY
        ORDER BY PLAYER_RANK
    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
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

    df = load_batting_data()

    if df.empty:

        st.warning(
            "No batting summary data available."
        )

    else:

        # ---------------------------------------------------------------------
        # Numeric Conversion
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

        df = df.sort_values(
            "PLAYER_RANK"
        )

        # =====================================================================
        # KPI CARDS
        # =====================================================================

        top_player = df.iloc[0]

        total_players = len(df)

        total_runs = int(
            df["TOTAL_RUNS"].sum()
        )

        total_fours = int(
            df["FOURS"].sum()
        )

        total_sixes = int(
            df["SIXES"].sum()
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🏆 Top Run Scorer",
                top_player["BATSMAN"]
            )

        with col2:

            st.metric(
                "🏏 Top Runs",
                f"{int(top_player['TOTAL_RUNS']):,}"
            )

        with col3:

            st.metric(
                "4️⃣ Total Fours",
                f"{total_fours:,}"
            )

        with col4:

            st.metric(
                "6️⃣ Total Sixes",
                f"{total_sixes:,}"
            )

        st.divider()

        # =====================================================================
        # TOP 10 RUN SCORERS
        # =====================================================================

        st.subheader(
            "🏆 Top 10 Run Scorers"
        )

        top_10 = (
            df
            .sort_values(
                "TOTAL_RUNS",
                ascending=False
            )
            .head(10)
            .sort_values(
                "TOTAL_RUNS"
            )
        )

        fig_runs = px.bar(
            top_10,
            x="TOTAL_RUNS",
            y="BATSMAN",
            orientation="h",
            text="TOTAL_RUNS",
            title="Top 10 IPL Run Scorers"
        )

        fig_runs.update_traces(
            textposition="outside"
        )

        fig_runs.update_layout(
            xaxis_title="Total Runs",
            yaxis_title="Batsman",
            showlegend=False
        )

        st.plotly_chart(
            fig_runs,
            use_container_width=True
        )

        # =====================================================================
        # RUNS VS STRIKE RATE
        # =====================================================================

        st.subheader(
            "⚡ Runs vs Strike Rate"
        )

        scatter_df = df.dropna(
            subset=[
                "TOTAL_RUNS",
                "STRIKE_RATE"
            ]
        ).copy()

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
            title="Total Runs vs Strike Rate"
        )

        fig_scatter.update_layout(
            xaxis_title="Total Runs",
            yaxis_title="Strike Rate"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

        # =====================================================================
        # TOP SIX HITTERS
        # =====================================================================

        st.subheader(
            "6️⃣ Top Six Hitters"
        )

        top_six = (
            df
            .sort_values(
                "SIXES",
                ascending=False
            )
            .head(10)
            .sort_values(
                "SIXES"
            )
        )

        fig_sixes = px.bar(
            top_six,
            x="SIXES",
            y="BATSMAN",
            orientation="h",
            text="SIXES",
            title="Top 10 Six Hitters"
        )

        fig_sixes.update_traces(
            textposition="outside"
        )

        fig_sixes.update_layout(
            xaxis_title="Sixes",
            yaxis_title="Batsman",
            showlegend=False
        )

        st.plotly_chart(
            fig_sixes,
            use_container_width=True
        )

        # =====================================================================
        # BATTING LEADERBOARD
        # =====================================================================

        st.subheader(
            "📊 Batting Leaderboard"
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
        "❌ Unable to load batting summary."
    )

    st.code(
        str(e)
    )
