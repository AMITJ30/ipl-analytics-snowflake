import streamlit as st

from utils.filters import show_sidebar_filters


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="IPL Analytics Platform",
    page_icon="🏏",
    layout="wide"
)


# -----------------------------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------------------------

selected_season, selected_team = show_sidebar_filters()


# -----------------------------------------------------------------------------
# Home Page
# -----------------------------------------------------------------------------

st.title("🏏 IPL Analytics Platform")

st.markdown(
    """
    ## Welcome

    This project demonstrates an end-to-end Data Engineering pipeline
    built on Snowflake.

    ### Architecture

    - 🥉 Bronze Layer
    - 🥈 Silver Layer
    - 🥇 Gold Layer
    - 📊 Reporting Layer

    Use the navigation menu on the left to explore the dashboards.
    """
)

st.success("Project setup completed successfully!")

st.write("Selected Season:", selected_season)
st.write("Selected Team:", selected_team)
