import streamlit as st
from sections import universities, documents, applications, questions, logins, payments

st.set_page_config(page_title="Student Dashboard", layout="wide")

section = st.sidebar.selectbox("📂 Go to section", [
    "Universities", "Documents", "Applications", "Questions", "Logins", "Payments"
])

if section == "Universities":
    universities.show()
elif section == "Documents":
    documents.show()
elif section == "Applications":
    applications.show()
elif section == "Questions":
    questions.show()
elif section == "Logins":
    logins.show()
elif section == "Payments":
    payments.show()
