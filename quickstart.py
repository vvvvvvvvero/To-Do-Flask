import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate():
    creds = None
    if os.path.exists('authentication/token.json'):
        creds = Credentials.from_authorized_user_file('authentication/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'authentication/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('authentication/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_calendar_service():
    creds = authenticate()
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    get_calendar_service()
