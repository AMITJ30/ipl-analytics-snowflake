import streamlit as st
import snowflake.connector

st.set_page_config(page_title="Snowflake Connection Test")

st.title("❄️ Snowflake Connection Test")

try:
    conn = snowflake.connector.connect(
        account=st.secrets["ACCOUNT"],
        user=st.secrets["USER"],
        password=st.secrets["PASSWORD"],
        warehouse=st.secrets["WAREHOUSE"],
        database=st.secrets["DATABASE"],
        schema=st.secrets["SCHEMA"],
        role=st.secrets["ROLE"],
    )

    st.success("✅ Connected to Snowflake successfully!")

    cur = conn.cursor()

    cur.execute("""
        SELECT
            CURRENT_ACCOUNT(),
            CURRENT_USER(),
            CURRENT_ROLE(),
            CURRENT_WAREHOUSE(),
            CURRENT_DATABASE(),
            CURRENT_SCHEMA(),
            CURRENT_VERSION()
    """)

    result = cur.fetchone()

    st.subheader("Connection Details")

    st.write(f"**Account:** {result[0]}")
    st.write(f"**User:** {result[1]}")
    st.write(f"**Role:** {result[2]}")
    st.write(f"**Warehouse:** {result[3]}")
    st.write(f"**Database:** {result[4]}")
    st.write(f"**Schema:** {result[5]}")
    st.write(f"**Snowflake Version:** {result[6]}")

    cur.close()
    conn.close()

except Exception as e:
    st.error("❌ Connection Failed")
    st.code(str(e))