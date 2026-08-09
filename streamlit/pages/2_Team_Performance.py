import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Team Performance",
    page_icon="🏆",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🏆 Team Performance")

st.markdown(
    """
    Analyze IPL team performance based on matches won.
    """
)


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_team_performance():

    conn = get_connection()

    query = """
        SELECT *
        FROM REPORTING.VW_TEAM_PERFORMANCE
        ORDER BY MATCHES_WON DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


try:

    df = load_team_performance()

    # -------------------------------------------------------------------------
    # Data Validation
    # -------------------------------------------------------------------------

    if df.empty:

        st.warning("No team performance data available.")

    else:

        # ---------------------------------------------------------------------
        # KPI
        # ---------------------------------------------------------------------

        total_teams = len(df)

        top_team = df.iloc[0]["TEAM"]

        top_wins = int(df.iloc[0]["MATCHES_WON"])


        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "👥 Teams",
                total_teams
            )

        with col2:
            st.metric(
                "🏆 Most Successful Team",
                top_team
            )

        with col3:
            st.metric(
                "🥇 Most Wins",
                f"{top_wins:,}"
            )


        st.divider()


        # ---------------------------------------------------------------------
        # Team Wins Chart
        # ---------------------------------------------------------------------

        st.subheader("🏆 Matches Won by Team")

        fig = px.bar(
            df,
            x="TEAM",
            y="MATCHES_WON",
            text="MATCHES_WON",
            title="IPL Matches Won by Team"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Team",
            yaxis_title="Matches Won",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ---------------------------------------------------------------------
        # Team Performance Table
        # ---------------------------------------------------------------------

        st.subheader("📊 Team Performance Details")

        display_df = df.copy()

        display_df["MATCHES_WON"] = display_df["MATCHES_WON"].astype(int)

        display_df = display_df.rename(
            columns={
                "TEAM": "Team",
                "MATCHES_WON": "Matches Won"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


except Exception as e:

    st.error("❌ Unable to load team performance data.")

    st.code(str(e))
