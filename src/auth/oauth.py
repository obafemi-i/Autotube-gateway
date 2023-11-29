import os
import sys
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


# Define the scopes needed for the YouTube Data API
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
        creds = Credentials.from_authorized_user_file('token1.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'desktop.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token1.json', 'w') as token:
            token.write(creds.to_json())

        youtube = build('youtube', 'v3', credentials=creds)
        return youtube
    
