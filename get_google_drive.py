import io
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/documents.readonly"]


def get_diary_list():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # Use service account credentials
    creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

    try:
        service = build("drive", "v3", credentials=creds)

        folder_id = os.environ.get("DRIVE_FOLDER_ID")

        # Call the Drive v3 API
        page_token = None
        while True:
            results = (
                service.files()
                .list(
                    q=f"'{folder_id}' in parents",
                    spaces="drive",
                    fields="nextPageToken, files(id, name, createdTime, modifiedTime)",
                    orderBy="modifiedTime desc",
                    pageSize=1000,  # 最大1000まで指定可能
                    pageToken=page_token,
                )
                .execute()
            )
            items = results.get("files", [])
            for item in items:
                print(f"{item['name']} ({item['id']}) ({item['createdTime']}) ({item['modifiedTime']})")

            page_token = results.get("nextPageToken", None)
            if page_token is None:
                break
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


def get_content_by_id(file_id):
    creds = None
    # Use service account credentials
    creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

    try:
        service = build("drive", "v3", credentials=creds)

        # Get file metadata
        file_metadata = service.files().get(fileId=file_id, fields="name, mimeType").execute()

        # Check if the file is a Google Doc
        if file_metadata["mimeType"] == "application/vnd.google-apps.document":
            # Export the file as plain text
            request = service.files().export_media(fileId=file_id, mimeType="text/plain")
        else:
            # For non-Google Doc files, just get the content
            request = service.files().get_media(fileId=file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        content = fh.getvalue().decode("utf-8")

        print(f"File Name: {file_metadata['name']}")
        print(f"MIME Type: {file_metadata['mimeType']}")
        print(f"Content: {content}")

        return content

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


if __name__ == "__main__":
    # get_diary_list()
    get_content_by_id("dummy file id")
