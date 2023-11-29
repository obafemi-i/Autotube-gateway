import os
import sys
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# The scope needed to upload videos using the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


# def request_creds():
#     creds = None
#     if os.path.exists('desktop.json'):
#         flow = InstalledAppFlow.from_client_secrets_file('desktop.json', SCOPES)
#         creds = flow.run_local_server(port=0)
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#         return Credentials.from_authorized_user_file('token.json', SCOPES)
#     else:
#         print('credentials not present')
#         sys.exit(1)


def authenticate_with_oauth():
    creds = None
    if os.path.exists('token1.json'):
        creds = Credentials.from_authorized_user_file('token1.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'desktop.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token1.json', 'w') as token:
            token.write(creds.to_json())

        youtube = build('youtube', 'v3', credentials=creds)
        return youtube
    


def upload_to_youtube(youtube, video_file, title, description, category_id, privacy_status='public'):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    # Perform video insert request
    insert_request = youtube.videos().insert(
        part = ",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(video_file, resumable=True)
    )

    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

        print(f"Video id '{response['id']}' was successfully uploaded.")
