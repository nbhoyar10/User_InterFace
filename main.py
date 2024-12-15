# Importing All required libraries
import requests
from PIL import Image
from io import BytesIO
import os
import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
#---------------------------------------------------------------------------#


st.set_page_config(page_title="Enzigma_UI",layout="wide")


#Header
st.header("Hey, I am Nirbhay Bhoyar")
st.title("Overview")
st.write("The project is a user-friendly web interface that allows team members to efficiently manage form submissions by "
         "uploading image or PDF files and accessing previously submitted records.")


with st.container():
    st.write("-----")
    left_column, right_column=st.columns(2)
    with left_column:
        st.header("File Upload Functionality:")
        st.write("""The interface supports the upload of image files (JPG, PNG) and PDF files.
                    Users can upload multiple files simultaneously for convenience.
                    The uploaded files are stored securely in Google Drive, with their metadata saved in Google Sheets.""")
with right_column:
    st.header("Records Management:")
    st.write(""""The interface provides a feature to view existing records stored in the database.
                 Users can search records by name or email, ensuring quick access to specific entries.
                 Upon selecting a record, the interface displays detailed information, including:
                 1-Candidate’s name and email.
                 2-Uploaded files with clickable links to access them directly from Google Drive.

         """)


# Configure Google Sheets and Google Drive API
SERVICE_ACCOUNT_FILE = "C:\\Users\\nirbh\\Downloads\\user-interface-enzigma-07998b8dfc33.json"  # Replace with your JSON credentials file
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Sheets API client
client = gspread.authorize(credentials)

# Google Drive API client
drive_service = build("drive", "v3", credentials=credentials)

# Google Sheet name and worksheet
SPREADSHEET_NAME = "EnzigmaDatabase"  # Replace with your Google Sheet name
try:
    sheet = client.open(SPREADSHEET_NAME).sheet1  # Access the first sheet
except gspread.SpreadsheetNotFound:
    st.error(f"Spreadsheet '{SPREADSHEET_NAME}' not found. Please create it in your Google Drive.")

# Google Drive folder ID (replace with your folder's ID from Google Drive)
DRIVE_FOLDER_ID = "1sS7lZNaBFk6jmWUIO5MywEzPmPgAc_z5"  # Replace this with the actual folder ID from Google Drive

# Function to upload files to Google Drive
def upload_to_drive(file_name, file_data, mime_type):
    try:
        file_metadata = {"name": file_name, "parents": [DRIVE_FOLDER_ID]}
        media = MediaIoBaseUpload(io.BytesIO(file_data), mimetype=mime_type)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
        return file.get("webViewLink")  # Return the link to the uploaded file
    except Exception as e:
        st.error(f"An error occurred while uploading to Google Drive: {e}")
        return None
# Set page title with emoji and color
st.markdown(
    "<h1 style='text-align: center; color: #FF6347;'>📄✨ Form Submission System ✨📄</h1>",
    unsafe_allow_html=True
)

# Section: Input Name and Email
st.markdown(
    "<h3 style='color: #4682B4;'>📝 Enter Your Details</h3>",
    unsafe_allow_html=True
)
name = st.text_input("Name 🧑‍💼", placeholder="Enter your full name")
email = st.text_input("Email 📧", placeholder="Enter your email address")

# Section: File Upload
st.markdown(
    "<h3 style='color: #4682B4;'>📤 Upload Files</h3>",
    unsafe_allow_html=True
)
uploaded_files = st.file_uploader(
    "Upload one or more files (Images or PDFs) 🖼️📂",
    type=["png", "jpg", "jpeg", "pdf"],
    accept_multiple_files=True
)

# Submit Button
if st.button("🚀 Submit"):
    if not name or not email:
        st.error("❌ Please fill out both Name and Email fields before submitting.")
    elif not uploaded_files:
        st.error("❌ Please upload at least one file before submitting.")
    else:
        st.info("⏳ Uploading files... Please wait.")
        upload_success = True

        # Save data to Google Sheets
        for uploaded_file in uploaded_files:
            file_data = uploaded_file.read()
            mime_type = uploaded_file.type

            # Upload file to Google Drive
            file_link = upload_to_drive(uploaded_file.name, file_data, mime_type)
            if file_link:
                # Add data to Google Sheet
                sheet.append_row([name, email, uploaded_file.name, mime_type, file_link])
            else:
                upload_success = False

        if upload_success:
            st.success("✅ Submission Successful!")
            st.markdown(
                f"""
                <p style='color: #228B22;'><strong>🎉 Thank you for your submission!</strong></p>
                <p><strong>Name:</strong> {name} 🧑‍💼</p>
                <p><strong>Email:</strong> {email} 📧</p>
                """,
                unsafe_allow_html=True
            )
            st.write("📁 **Uploaded Files:**")

            # Display uploaded files and their Google Drive links
            # for uploaded_file in uploaded_files:
            #     st.write(f"- {uploaded_file.name}")
            #     if uploaded_file.type.startswith("image"):
            #         # img = Image.open(io.BytesIO(uploaded_file.read()))
            #         st.image(img, caption=uploaded_file.name)
            #         st.image(img, caption=uploaded_file.name, use_column_width=True)

            st.markdown("<h3 style='text-align: center;'>🎈 We appreciate your contribution! 🎈</h3>", unsafe_allow_html=True)
        else:
            st.error("❌ An error occurred while uploading one or more files. Please try again.")

            # TO RUN THIS CODE USE ---- [streamlit run main.py]
