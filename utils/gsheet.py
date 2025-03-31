
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Scopes and credentials
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(CREDS)

def get_worksheet_df(sheet_url, tab_name):
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(tab_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def update_cell_by_value(sheet_url, tab_name, document_name, updates: dict):
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(tab_name)
    data = worksheet.get_all_records()

    # Find row index where Document Name matches
    for i, row in enumerate(data):
        if row["Document Name"] == document_name:
            for key, value in updates.items():
                col_index = list(row.keys()).index(key) + 1
                worksheet.update_cell(i + 2, col_index, value)  # +2 because rows start at 1 and row[0] is headers
            break
