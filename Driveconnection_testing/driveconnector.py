from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import io
from googleapiclient.http import MediaIoBaseDownload
import shutil

creds = None
SCOPES = ['https://www.googleapis.com/auth/drive']
if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('drive', 'v3', credentials=creds)

# file_id = '1qZb8wbJudVIiTvHSojY33YkzgrkmzxfH'
def FileUpload(file_name):
    # request = service.files().get_media(fileId=file_id)
    # fh = io.FileIO('test.mp3', 'wb')
    # downloader = MediaIoBaseDownload(fh, request)
    # done = False
    # while done is False:
    #     status, done = downloader.next_chunk()
    #     print ("Download %d%%." % int(status.progress() * 100))

    file_metadata = {'name': file_name, 'parents': ['1fLldujG9j82no3x9hYlsat6Vw8FQTsZ-']}
    media = MediaFileUpload(file_name, mimetype='text/txt')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print ('File ID: %s' % file.get('id'))

def searchfolder():
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)",q="'1fLldujG9j82no3x9hYlsat6Vw8FQTsZ-' in parents").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')

    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))

def FileDownload(file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    # Initialise a downloader object to download the file
    downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
    done = False
    try:
        # Download the data in chunks
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        # Write the received data to the file
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(fh, f)
        print("File Downloaded")
        # Return True if file Downloaded successfully
        return True
    except:
        # Return False if something went wrong
        print("Something went wrong.")
        return False

# searchfolder()
# FileDownload('1n8k_nViWmi9bwIhQ0tQ2hGR_5FBQ0Qrd', 'test.mp3')
FileUpload('test.txt')