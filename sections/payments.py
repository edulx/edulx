import streamlit as st
import pandas as pd
from utils.gsheet import get_worksheet_df

def show():
    st.header("💳 Payment Summary")

    sheet_url = st.secrets["student_sheet_url"]
    df = get_worksheet_df(sheet_url, "Payments")

    if df.empty:
        st.info("No payment records found.")
        return

    # Optional: Convert amount to numeric for totals
    df["Amount (INR)"] = pd.to_numeric(df["Amount (INR)"], errors="coerce").fillna(0)

    total_paid = df[df["Status"].str.lower() == "paid"]["Amount (INR)"].sum()
    total_due = df[df["Status"].str.lower() == "pending"]["Amount (INR)"].sum()

    col1, col2 = st.columns(2)
    col1.metric("✅ Total Paid", f"₹{total_paid:,.0f}")
    col2.metric("🕒 Pending Dues", f"₹{total_due:,.0f}")

    st.markdown("### 📄 Payment History")
    st.dataframe(df, use_container_width=True)
