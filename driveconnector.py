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
from google.oauth2 import service_account
import shutil


from py_SQL import db_connection

db, mycursor = db_connection()

creds = None
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'ServiceAccount.json'
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# create an object
service = build('drive', 'v3', credentials=creds)
# file_id = '1qZb8wbJudVIiTvHSojY33YkzgrkmzxfH'

# get file path
def FileUpload(file_name, uid, file_path):
    flag = False
    checkupload = f"select subscription, uploaded from user_tbl where uid = '{uid}'"
    mycursor.execute(checkupload)
    myresult = mycursor.fetchall()
    for i in myresult:
        if i[0]==False:
            if i[1]>=15:
                flag = False
                print('sth')
            else:
                flag = True
        elif i[0]==True:
            flag = True
    if flag == True:
        file_metadata = {'name': file_name, 'parents': ['1fLldujG9j82no3x9hYlsat6Vw8FQTsZ-']}#to send the data to google drive
        media = MediaFileUpload(file_path, mimetype='audio/mpeg')#specify the file type 
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()#execution 
        uploadid = ('%s' % file.get('id'))#get the file id
        newupload = i[1]+1
        upload_update = f"Update user_tbl set uploaded = {newupload} where uid = '{uid}'"
        mycursor.execute(upload_update)
        db.commit()
        return uploadid
    else:
        return ("Upload Declined")

def searchfolder():
    results = service.files().list(
        pageSize=100, fields="nextPageToken, files(id, name)",q="'1fLldujG9j82no3x9hYlsat6Vw8FQTsZ-' in parents").execute()
    items = results.get('files', [])
    print(items)
    if not items:
        print('No files found.')

    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))

def FileDownload(file_id, file_name, Username):
    flag = False
    check_download = f"select username, subscription, downloaded from user_tbl where username = '{Username}'"
    mycursor.execute(check_download)
    myresult = mycursor.fetchall()
    for i in myresult:
        if i[1]==False:
            if i[2]>=15:
                flag = False
            else:
                flag = True
        elif i[1]==True:
            flag = True
    if flag == True:
        request = service.files().get_media(fileId=file_id)#request id on the thing u want download
        fh = io.BytesIO()
        # Initialise a downloader object to download the file
        downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
        done = False
        #LOOP IF NOT DOWNLOADED FINISH IT WILL KEEP LOOPING
        try:
            # Download the data in chunks
            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)
            # Write the received data to the file
            path = 'audio_files'

            if not os.path.exists(path):
                os.makedirs(path)

            with open(os.path.join(path, file_name), 'wb') as f:
                shutil.copyfileobj(fh, f)
            
            newdownload = i[2]+1
            print(i[2])
            download_update = f"Update user_tbl set downloaded = {newdownload} where username = '{Username}'"
            mycursor.execute(download_update)
            db.commit()

            print("File Downloaded")
            # Return True if file Downloaded successfully
            return True
        except:
            # Return False if something went wrong
            print("Something went wrong.")
            return False
    else:
        return ("Download Declined")

def ImageDownload(image_id, image_name):
    request = service.files().get_media(fileId=image_id)
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
        path = 'image'

        if not os.path.exists(path):
            os.makedirs(path)

        with open(os.path.join(path, image_name), 'wb') as f:
            shutil.copyfileobj(fh, f)
        print("File Downloaded")
        # Return True if file Downloaded successfully
        return True
    except:
        # Return False if something went wrong
        print("Something went wrong.")
        return False

def ImageUpload(image_name, user_id):
    uploadname = str(user_id)+'.jpg'
    file_metadata = {'name': uploadname, 'parents': ['1oVNqxZLgKijznqNPNtjQrdqq84iX4Dua']}#to send the data to google drive
    media = MediaFileUpload(image_name, mimetype = 'image/jpeg' or 'image/png')#specify the file type 
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()#execution 
    uploadid = file.get('id')#get the file id
    return uploadid

searchfolder()
# FileDownload()
# print(FileDownload('1VVKlc1ecmpJs2arxxhlvsBovgv9hAitw', 'test.mp3','admin'))
# print(FileUpload('test1',2, 'test.mp3'))
# a = ImageUpload('a.png', 1)
# ImageDownload(a, 'test2.jpg')