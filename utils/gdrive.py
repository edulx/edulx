import io
import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Use credentials from Streamlit secrets
SCOPES = ["https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
drive_service = build("drive", "v3", credentials=CREDS)

def upload_file_to_drive(uploaded_file, folder_id):
    file_metadata = {
        "name": uploaded_file.name,
        "parents": [folder_id]
    }

    media = MediaIoBaseUpload(io.BytesIO(uploaded_file.getvalue()), mimetype=uploaded_file.type)
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    # Make file public
    drive_service.permissions().create(
        fileId=file["id"],
        body={"type": "anyone", "role": "reader"},
    ).execute()

    return f"https://drive.google.com/file/d/{file['id']}/view"
