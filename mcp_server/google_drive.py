from io import BytesIO
from pathlib import Path

import fitz
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]

CREDENTIALS_PATH = Path(__file__).resolve().parents[1] / "credentials.json"

GOOGLE_FILE_EXPORTS = {
    "application/vnd.google-apps.document": "text/plain",
    "application/vnd.google-apps.spreadsheet": "text/csv",
    "application/vnd.google-apps.presentation": "text/plain",
}


def get_drive_service():

    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=SCOPES
    )

    service = build(
        "drive",
        "v3",
        credentials=credentials
    )

    return service

#downloads the exported content
def _download(request):
    buffer = BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False

    while not done:
        _, done = downloader.next_chunk()

    return buffer.getvalue()


def _extract_pdf_text(data):
    with fitz.open(stream=data, filetype="pdf") as document:
        text = "\n".join(page.get_text() for page in document)

    if not text.strip():
        raise ValueError(
            "The PDF contains no extractable text. "
            "A scanned PDF must be processed with OCR first."
        )

    return text

def search_pdf(subject: str, topic: str) -> str:
    """
    Search Google Drive for a PDF using subject and topic.
    Returns the Google Drive file ID.
    """

    service = get_drive_service()

    # Find the subject folder
    folder_query = (
        f"name='{subject}' and "
        "mimeType='application/vnd.google-apps.folder' and "
        "trashed=false"
    )

    folders = service.files().list(
        q=folder_query,
        fields="files(id,name)"
    ).execute()

    if not folders["files"]:
        raise Exception(f"Subject folder '{subject}' not found.")

    subject_folder_id = folders["files"][0]["id"]

    # Search for the PDF inside the subject folder
    pdf_query = (
        f"'{subject_folder_id}' in parents and "
        f"name contains '{topic}' and "
        "trashed=false"
    )

    results = service.files().list(
        q=pdf_query,
        fields="files(id,name,mimeType)"
    ).execute()

    files = results.get("files", [])

    if not files:
        raise Exception(
            f"No PDF found for topic '{topic}' in subject '{subject}'."
        )

    print("Found:", files[0]["name"])

    return files[0]["id"]


def read_google_drive(file_id: str) -> str:
    """Download a Drive file and return lesson content as text."""

    service = get_drive_service()

    file_metadata = service.files().get(
        fileId=file_id,
        fields="name,mimeType"
    ).execute()

    name = file_metadata["name"]
    mime_type = file_metadata["mimeType"]
    print("Reading:", name)

    if mime_type in GOOGLE_FILE_EXPORTS:
        export_type = GOOGLE_FILE_EXPORTS[mime_type]
        request = service.files().export_media(
            fileId=file_id,
            mimeType=export_type
        )
        return _download(request).decode("utf-8") #converted to a Python string using:

    request = service.files().get_media(fileId=file_id)
    content = _download(request)

    if mime_type == "application/pdf" or name.lower().endswith(".pdf"):
        return _extract_pdf_text(content)

    if mime_type.startswith("text/"):
        return content.decode("utf-8") #Convert the downloaded bytes into normal readable text using UTF-8 encoding.

    raise ValueError(
        f"Unsupported Drive file type: {mime_type} ({name})"
    )
