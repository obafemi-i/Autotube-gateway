import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials


# Define the scopes needed for the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def request_creds():
    creds = None
    if os.path.exists('desktop.json'):
        flow = InstalledAppFlow.from_client_secrets_file('desktop.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        return Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print('credentials not present')
        sys.exit(1)

