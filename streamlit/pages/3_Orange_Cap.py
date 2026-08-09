import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Orange Cap",
    page_icon="🏏",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🏏 Orange Cap")

st.markdown(
    "Explore the leading IPL run scorers and their batting performance."
)


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_orange_cap():

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
        FROM REPORTING.VW_ORANGE_CAP
        ORDER BY PLAYER_RANK
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

try:

    df = load_orange_cap()

    if df.empty:

        st.warning("No Orange Cap data available.")

    else:

        # ---------------------------------------------------------------------
        # Top Player
        # ---------------------------------------------------------------------

        top_player = df.iloc[0]

        # ---------------------------------------------------------------------
        # KPI Cards
        # ---------------------------------------------------------------------

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
            st.metric(
                "⚡ Strike Rate",
                f"{float(top_player['STRIKE_RATE']):.2f}"
            )

        with col4:
            st.metric(
                "📊 Batting Average",
                f"{float(top_player['BATTING_AVERAGE']):.2f}"
            )

        st.divider()

        # ---------------------------------------------------------------------
        # Top 10 Run Scorers
        # ---------------------------------------------------------------------

        st.subheader("🏆 Top 10 Run Scorers")

        top_10 = df.head(10)

        fig = px.bar(
            top_10.sort_values("TOTAL_RUNS"),
            x="TOTAL_RUNS",
            y="BATSMAN",
            orientation="h",
            text="TOTAL_RUNS",
            title="Top 10 IPL Run Scorers"
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

        # ---------------------------------------------------------------------
        # Strike Rate vs Runs
        # ---------------------------------------------------------------------

        st.subheader("⚡ Strike Rate vs Total Runs")

        fig_scatter = px.scatter(
            df.head(50),
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
            title="Runs vs Strike Rate — Top 50 Players"
        )

        fig_scatter.update_layout(
            xaxis_title="Total Runs",
            yaxis_title="Strike Rate"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Detailed Table
        # ---------------------------------------------------------------------

        st.subheader("📊 Orange Cap Leaderboard")

        display_df = df.copy()

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

        display_df["Strike Rate"] = display_df["Strike Rate"].round(2)

        display_df["Batting Average"] = (
            display_df["Batting Average"].round(2)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


except Exception as e:

    st.error("❌ Unable to load Orange Cap data.")

    st.code(str(e))
