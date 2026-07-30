import streamlit as st
import snowflake.connector


def get_connection():

    conn = snowflake.connector.connect(
        account=st.secrets["ACCOUNT"],
        user=st.secrets["USER"],
        password=st.secrets["PASSWORD"],
        warehouse=st.secrets["WAREHOUSE"],
        database=st.secrets["DATABASE"],
        schema=st.secrets["SCHEMA"],
        role=st.secrets["ROLE"],
    )

    return conn
