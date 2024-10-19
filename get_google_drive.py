from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # Use service account credentials
    creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

    try:
        service = build("drive", "v3", credentials=creds)

        drive_folder_id = os.environ.get("DRIVE_FOLDER_ID")

        # Call the Drive v3 API
        results = (
            service.files()
            # .list(pageSize=10, fields="nextPageToken, files(id, name, createdTime, modifiedTime)")
            .list(pageSize=10,driveId=drive_folder_id,orderBy="name desc")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return
        print("Files:")
        for item in items:
            import json
            print(json.dumps(item, indent=4, ensure_ascii=False))

            # print(f"{item['name']} ({item['id']}) ({item['createdTime']}) ({item['modifiedTime']})")
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
