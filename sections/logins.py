import streamlit as st
import pandas as pd
import gspread
from utils.gsheet import get_worksheet_df

def show():
    st.header("🔐 University Login Details")

    sheet_url = st.secrets["student_sheet_url"]
    gc = gspread.service_account(filename="credentials.json")
    sheet = gc.open_by_url(sheet_url)
    worksheet = sheet.worksheet("Logins")

    # Existing data
    df = worksheet.get_all_records()
    if df:
        st.markdown("### 🧾 Saved Logins")
        st.dataframe(pd.DataFrame(df), use_container_width=True)

    st.markdown("---")
    st.markdown("### ➕ Add a New Login")

    with st.form("add_login"):
        url = st.text_input("University Portal URL")
        username = st.text_input("Username")
        password = st.text_input("Password")
        comment = st.text_input("Comment / Notes")

        submitted = st.form_submit_button("Save Login")
        if submitted:
            if url and username and password:
                worksheet.append_row([url, username, password, comment])
                st.success("Login saved successfully. Refresh to see it above.")
            else:
                st.error("Please fill in all required fields.")
