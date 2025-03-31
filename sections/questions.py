import streamlit as st
from utils.gsheet import get_worksheet_df
import gspread
import pandas as pd

def show():
    st.header("❓ SOP / Profile Questions")

    # Input student info
    student_name = st.text_input("Your Full Name")
    email = st.text_input("Your Email")

    if not student_name or not email:
        st.warning("Please enter your name and email to continue.")
        return

    sheet_url = st.secrets["student_sheet_url"]
    gc = gspread.service_account(filename="credentials.json")
    sheet = gc.open_by_url(sheet_url)
    worksheet = sheet.worksheet("Questions")

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    # Check if student already exists
    student_row_index = None
    for i, row in enumerate(data):
        if row.get("Email", "").lower() == email.lower():
            student_row_index = i + 2  # +2 = 1 for headers, 1 for 1-based index
            break

    # Get list of question columns
    question_cols = [col for col in df.columns if col not in ["Student Name", "Email"]]

    with st.form("questions_form"):
        answers = {}
        for col in question_cols:
            question_label = col
            default = df.loc[df["Email"].str.lower() == email.lower(), col].values[0] if email.lower() in df["Email"].str.lower().values else ""
            answers[col] = st.text_area(question_label, value=default)

        submitted = st.form_submit_button("Save My Answers")

    if submitted:
        values = [student_name, email] + [answers[col] for col in question_cols]
        if student_row_index:  # update existing
            worksheet.update(f"A{student_row_index}", [values])
            st.success("Answers updated successfully.")
        else:  # append new
            worksheet.append_row(values)
            st.success("Answers submitted successfully.")
