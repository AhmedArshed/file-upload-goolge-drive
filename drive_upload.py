from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


def remove_dublicate(name):
    stock = pd.read_csv(name, low_memory=False)
    stock.drop_duplicates(inplace=True)
    stock.to_csv(name, index=False)
    return stock


def upload(name, id):
    remove_dublicate(name)
    creds = None

    '''The file token.pickle stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.'''

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            file = os.path.join(os.path.dirname(__file__), 'credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(
                file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    folder_id = '1UOZNE9GEHGGBYSuyOjsfu8v82MFCKrHE'
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': name,
                     'parents': [id]
                     }

    media = MediaFileUpload(name, mimetype='sheets/csv')
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print('File ID: %s' % file.get('id'))
