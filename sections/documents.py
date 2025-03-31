import streamlit as st
import pandas as pd
import datetime
from utils.gsheet import get_worksheet_df, update_cell_by_value
from utils.gdrive import upload_file_to_drive

def show():
    st.header("📄 Upload Documents")
    sheet_url = st.secrets["student_sheet_url"]
    drive_folder = st.secrets["drive_folder_id"]

    df = get_worksheet_df(sheet_url, "Documents")

    for idx, row in df.iterrows():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**{row['Document Name']}** {'🟥 Required' if row['Required?'] == 'Yes' else ''}")
            notes = st.text_input(f"Notes for {row['Document Name']}", key=f"note_{idx}")
        with col2:
            uploaded = st.file_uploader(f"Upload {row['Document Name']}", type=["pdf", "png", "jpg"], key=f"file_{idx}")

        if uploaded:
            # Upload to Drive
            file_url = upload_file_to_drive(uploaded, drive_folder)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            # Update in sheet
            update_cell_by_value(sheet_url, "Documents", row['Document Name'], {
                "Uploaded?": "Yes",
                "Google Drive Link": file_url,
                "Last Updated": timestamp,
                "Notes": notes
            })
            st.success(f"{row['Document Name']} uploaded successfully.")
