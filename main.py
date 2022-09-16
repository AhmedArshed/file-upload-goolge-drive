from drive_upload import *
from creating_remote_folder_google_drive import *
from datetime import datetime, date
STATUS = "initial"


def main(id, useremial, identifier):
    try:
        global STATUS
        STATUS = "running"
        now = datetime.now()
        start_time = now.strftime("%H:%M:%S")
        
        folder_id = createRemoteFolder(identifier)
        ## any file
        file_name = 'xyz.csv'
        upload(file_name, folder_id)
        now = datetime.now()
        end_time = now.strftime("%H:%M:%S")
        folder_id = 'https://drive.google.com/open?id=' + folder_id
        STATUS = "idle"
        print(STATUS)
    except Exception as e:
        print(e)
def get_status():
    return STATUS
