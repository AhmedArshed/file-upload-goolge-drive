from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd


def createRemoteFolder(folderName):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            file = os.path.join(os.path.dirname(__file__), 'credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(
                file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    folder_id = '1UOZNE9GEHGGBYSuyOjsfu8v82MFCKrHE'
    service = build('drive', 'v3', credentials=creds)

    body = {
        'name': folderName,
        'title': folderName,
        'mimeType': "application/vnd.google-apps.folder"
    }
    if folder_id:
        body['parents'] = [{'id': folder_id}]
    root_folder = service.files().create(body=body).execute()
    permission = {'type': 'anyone',
                  'value': 'anyone',
                  'role': 'reader'}
    service.permissions().create(
        fileId=root_folder['id'], body=permission).execute()
    return root_folder['id']
