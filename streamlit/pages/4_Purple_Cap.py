import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Purple Cap",
    page_icon="🎯",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🎯 Purple Cap")

st.markdown(
    "Explore the leading IPL wicket-takers and their bowling performance."
)


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_purple_cap():

    conn = get_connection()

    query = """
        SELECT
            PLAYER_RANK,
            BOWLER,
            WICKETS,
            BALLS_BOWLED,
            RUNS_CONCEDED,
            DOT_BALLS,
            ECONOMY,
            BOWLING_STRIKE_RATE,
            BOWLING_AVERAGE
        FROM REPORTING.VW_PURPLE_CAP
        ORDER BY PLAYER_RANK
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

try:

    df = load_purple_cap()

    if df.empty:

        st.warning("No Purple Cap data available.")

    else:

        # ---------------------------------------------------------------------
        # Top Bowler
        # ---------------------------------------------------------------------

        top_bowler = df.iloc[0]

        # ---------------------------------------------------------------------
        # KPI Cards
        # ---------------------------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🏆 Top Wicket Taker",
                top_bowler["BOWLER"]
            )

        with col2:
            st.metric(
                "🎯 Wickets",
                f"{int(top_bowler['WICKETS']):,}"
            )

        with col3:
            st.metric(
                "📉 Economy",
                f"{float(top_bowler['ECONOMY']):.2f}"
            )

        with col4:
            st.metric(
                "⚡ Bowling Strike Rate",
                f"{float(top_bowler['BOWLING_STRIKE_RATE']):.2f}"
            )

        st.divider()

        # ---------------------------------------------------------------------
        # Top 10 Wicket Takers
        # ---------------------------------------------------------------------

        st.subheader("🏆 Top 10 Wicket Takers")

        top_10 = df.head(10)

        fig = px.bar(
            top_10.sort_values("WICKETS"),
            x="WICKETS",
            y="BOWLER",
            orientation="h",
            text="WICKETS",
            title="Top 10 IPL Wicket Takers"
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

        # ---------------------------------------------------------------------
        # Economy vs Wickets
        # ---------------------------------------------------------------------

        st.subheader("📊 Economy vs Wickets")

        fig_scatter = px.scatter(
            df.head(50),
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
            title="Wickets vs Economy — Top 50 Bowlers"
        )

        fig_scatter.update_layout(
            xaxis_title="Wickets",
            yaxis_title="Economy Rate"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Detailed Table
        # ---------------------------------------------------------------------

        st.subheader("📊 Purple Cap Leaderboard")

        display_df = df.copy()

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

        display_df["Economy"] = (
            display_df["Economy"].round(2)
        )

        display_df["Bowling Strike Rate"] = (
            display_df["Bowling Strike Rate"].round(2)
        )

        display_df["Bowling Average"] = (
            display_df["Bowling Average"].round(2)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


except Exception as e:

    st.error("❌ Unable to load Purple Cap data.")

    st.code(str(e))
