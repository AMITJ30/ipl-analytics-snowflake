import streamlit as st
import pandas as pd
import plotly.express as px

from utils.connection import get_connection
from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Team Performance",
    page_icon="🏆",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Global Filters
# -----------------------------------------------------------------------------

selected_season, selected_team = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------

st.title("🏆 Team Performance")

if selected_team == "All Teams":
    st.markdown("Analyze performance across all IPL teams.")
else:
    st.markdown(f"Showing performance for **{selected_team}**.")


# -----------------------------------------------------------------------------
# Load Data
# -----------------------------------------------------------------------------

@st.cache_data
def load_team_performance(team):

    conn = get_connection()

    if team == "All Teams":

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

    else:

        query = """
            SELECT
                TEAM_NAME,
                MATCHES_PLAYED,
                MATCHES_WON,
                MATCHES_LOST,
                WIN_PERCENTAGE
            FROM REPORTING.VW_TEAM_PERFORMANCE
            WHERE TEAM_NAME = %s
        """

        cursor = conn.cursor()

        cursor.execute(query, (team,))

        rows = cursor.fetchall()

        columns = [
            "TEAM_NAME",
            "MATCHES_PLAYED",
            "MATCHES_WON",
            "MATCHES_LOST",
            "WIN_PERCENTAGE"
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

    df = load_team_performance(selected_team)

    if df.empty:

        st.warning("No team performance data available.")

    else:

        # ---------------------------------------------------------------------
        # KPI Calculations
        # ---------------------------------------------------------------------

        total_teams = len(df)

        total_matches = int(
            df["MATCHES_PLAYED"].sum()
        )

        total_wins = int(
            df["MATCHES_WON"].sum()
        )

        average_win_percentage = float(
            df["WIN_PERCENTAGE"].mean()
        )

        # ---------------------------------------------------------------------
        # KPI Cards
        # ---------------------------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👥 Teams",
                total_teams
            )

        with col2:
            st.metric(
                "🏏 Matches Played",
                f"{total_matches:,}"
            )

        with col3:
            st.metric(
                "🏆 Matches Won",
                f"{total_wins:,}"
            )

        with col4:
            st.metric(
                "📈 Win Percentage",
                f"{average_win_percentage:.2f}%"
            )

        st.divider()

        # ---------------------------------------------------------------------
        # Win Percentage Chart
        # ---------------------------------------------------------------------

        st.subheader("📈 Win Percentage")

        chart_df = df.sort_values(
            "WIN_PERCENTAGE",
            ascending=True
        )

        fig = px.bar(
            chart_df,
            x="WIN_PERCENTAGE",
            y="TEAM_NAME",
            orientation="h",
            text="WIN_PERCENTAGE",
            title="Team Win Percentage"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Win Percentage (%)",
            yaxis_title="Team",
            xaxis=dict(range=[0, 100]),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ---------------------------------------------------------------------
        # Wins vs Losses
        # ---------------------------------------------------------------------

        st.subheader("🏆 Wins vs Losses")

        comparison_df = df[
            [
                "TEAM_NAME",
                "MATCHES_WON",
                "MATCHES_LOST"
            ]
        ].copy()

        comparison_df = comparison_df.melt(
            id_vars="TEAM_NAME",
            var_name="Result",
            value_name="Matches"
        )

        fig_comparison = px.bar(
            comparison_df,
            x="TEAM_NAME",
            y="Matches",
            color="Result",
            barmode="group",
            text="Matches",
            title="Matches Won vs Lost"
        )

        fig_comparison.update_layout(
            xaxis_title="Team",
            yaxis_title="Matches"
        )

        st.plotly_chart(
            fig_comparison,
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
