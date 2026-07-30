import streamlit as st

st.set_page_config(
    page_title="IPL Analytics Platform",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Analytics Platform")

st.markdown("""
## Welcome

This project demonstrates an end-to-end Data Engineering pipeline built on Snowflake.

### Architecture

- 🥉 Bronze Layer
- 🥈 Silver Layer
- 🥇 Gold Layer
- 📊 Reporting Layer

Use the navigation menu on the left to explore the dashboards.
""")

st.success("Project setup completed successfully!")