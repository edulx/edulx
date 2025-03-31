import streamlit as st
import pandas as pd
from utils.gsheet import get_worksheet_df

def show():
    st.header("📥 Applications Overview")

    sheet_url = st.secrets["student_sheet_url"]
    df = get_worksheet_df(sheet_url, "Applications")

    if df.empty:
        st.info("No applications data found.")
        return

    # Format university links
    if "University link" in df.columns:
        df["University link"] = df["University link"].apply(
            lambda x: f"[Link]({x})" if pd.notnull(x) else ""
        )

    # Optional: Sort by Priority or Deadline
    if "Priority" in df.columns:
        df = df.sort_values(by="Priority", ascending=True)

    st.dataframe(df, use_container_width=True)
