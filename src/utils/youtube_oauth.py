import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# The scope needed to upload videos using the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def authenticate_with_oauth():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # If there are no (valid) credentials availabe, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'desktop.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for the next run to avoid logging in every time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
        # Create and return Youtube API service object
        youtube = build('youtube', 'v3', credentials=creds)
        return youtube
    
