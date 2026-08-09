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
    "Analyze IPL team performance based on matches played, wins, losses and win percentage."
)


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_team_performance():

    conn = get_connection()

    query = """
        SELECT
            TEAM_NAME,
            MATCHES_PLAYED,
            MATCHES_WON,
            MATCHES_LOST,
            WIN_PERCENTAGE
        FROM REPORTING.VW_TEAM_PERFORMANCE
        ORDER BY WIN_PERCENTAGE DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

try:

    df = load_team_performance()

    if df.empty:

        st.warning("No team performance data available.")

    else:

        # ---------------------------------------------------------------------
        # Top Team
        # ---------------------------------------------------------------------

        top_team = df.iloc[0]["TEAM_NAME"]
        top_win_percentage = df.iloc[0]["WIN_PERCENTAGE"]

        # ---------------------------------------------------------------------
        # KPI Cards
        # ---------------------------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👥 Teams",
                len(df)
            )

        with col2:
            st.metric(
                "🏆 Top Team",
                top_team
            )

        with col3:
            st.metric(
                "🥇 Matches Won",
                f"{int(df.iloc[0]['MATCHES_WON']):,}"
            )

        with col4:
            st.metric(
                "📈 Best Win %",
                f"{float(top_win_percentage):.2f}%"
            )

        st.divider()

        # ---------------------------------------------------------------------
        # Win Percentage Chart
        # ---------------------------------------------------------------------

        st.subheader("📈 Team Win Percentage")

        fig = px.bar(
            df,
            x="TEAM_NAME",
            y="WIN_PERCENTAGE",
            text="WIN_PERCENTAGE",
            title="Win Percentage by Team"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Team",
            yaxis_title="Win Percentage (%)",
            yaxis=dict(range=[0, 100]),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Matches Won Chart
        # ---------------------------------------------------------------------

        st.subheader("🏆 Matches Won by Team")

        fig_wins = px.bar(
            df.sort_values("MATCHES_WON", ascending=False),
            x="TEAM_NAME",
            y="MATCHES_WON",
            text="MATCHES_WON",
            title="Total Matches Won"
        )

        fig_wins.update_traces(
            textposition="outside"
        )

        fig_wins.update_layout(
            xaxis_title="Team",
            yaxis_title="Matches Won",
            showlegend=False
        )

        st.plotly_chart(
            fig_wins,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Detailed Table
        # ---------------------------------------------------------------------

        st.subheader("📊 Team Performance Details")

        display_df = df.copy()

        display_df = display_df.rename(
            columns={
                "TEAM_NAME": "Team",
                "MATCHES_PLAYED": "Matches Played",
                "MATCHES_WON": "Matches Won",
                "MATCHES_LOST": "Matches Lost",
                "WIN_PERCENTAGE": "Win Percentage"
            }
        )

        display_df["Win Percentage"] = (
            display_df["Win Percentage"].round(2)
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


except Exception as e:

    st.error("❌ Unable to load team performance data.")

    st.code(str(e))
