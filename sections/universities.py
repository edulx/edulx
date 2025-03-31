import streamlit as st
from utils.gsheet import get_worksheet_df
import pandas as pd

def show():
    st.header("🏫 List of Possible Universities")

    sheet_url = st.secrets["student_sheet_url"]
    df = get_worksheet_df(sheet_url, "Universities")

    if df.empty:
        st.info("No universities found.")
        return

    # Filters
    with st.expander("🔍 Filters"):
        col1, col2, col3, col4 = st.columns(4)
        city_filter = col1.multiselect("City", sorted(df["City"].dropna().unique()))
        course_filter = col2.multiselect("Course", sorted(df["Course"].dropna().unique()))
        intake_filter = col3.multiselect("Intake", sorted(df["Intake"].dropna().unique()))
        priority_filter = col4.multiselect("Priority", sorted(df["Priority"].dropna().unique()))

    # Apply filters
    filtered_df = df.copy()
    if city_filter:
        filtered_df = filtered_df[filtered_df["City"].isin(city_filter)]
    if course_filter:
        filtered_df = filtered_df[filtered_df["Course"].isin(course_filter)]
    if intake_filter:
        filtered_df = filtered_df[filtered_df["Intake"].isin(intake_filter)]
    if priority_filter:
        filtered_df = filtered_df[filtered_df["Priority"].isin(priority_filter)]

    # Add university link as clickable URL
    if "University link" in filtered_df.columns:
        filtered_df["University link"] = filtered_df["University link"].apply(
            lambda x: f"[Link]({x})" if pd.notnull(x) else ""
        )

    st.dataframe(filtered_df, use_container_width=True)
