import streamlit as st
import snowflake.connector

try:
    conn = snowflake.connector.connect(
        account=st.secrets["snowflake"]["ACCOUNT"],
        user=st.secrets["snowflake"]["USER"],
        password=st.secrets["snowflake"]["PASSWORD"],
        warehouse=st.secrets["snowflake"]["WAREHOUSE"],
        database=st.secrets["snowflake"]["DATABASE"],
        schema=st.secrets["snowflake"]["SCHEMA"],
        role=st.secrets["snowflake"]["ROLE"],
    )

    print("✅ Connected successfully!")

    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_VERSION()")
    print("Snowflake Version:", cursor.fetchone()[0])

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed")
    print(e)
