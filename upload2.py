import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scope and API version
SCOPES = ['https://www.googleapis.com/auth/drive']
API_VERSION = 'v3'

def authenticate_google_drive():
    """Authenticate with the Google Drive API"""
    creds = None

    # Check if credentials file exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If credentials are not valid or don't exist, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/home/michael/CSF/CSFCode/Private/CSFPrivate/client_secret_689440254843-1vhe1uiabjtjgc7ru2a0laqb15huje03.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', API_VERSION, credentials=creds)

def upload_photo(drive_service, photo_path, folder_id=None):
    """Upload a photo to Google Drive"""
    file_metadata = {
        'name': os.path.basename(photo_path),
        'parents': [folder_id] if folder_id else None
    }

    media = drive_service.files().create(
        body=file_metadata,
        media_body=photo_path,
        fields='id'
    ).execute()

    print(f'Uploaded photo: {photo_path} (ID: {media["id"]})')

def main():
    # Authenticate with Google Drive
    drive_service = authenticate_google_drive()
    print('AuthDone')
    # Specify the folder ID where you want to upload the photos (optional)
    folder_id = '13-GcLY2F0KkF1xD6ua0EN4aeCRplMQrJ'#'13-GcLY2F0KkF1xD6ua0EN4aeCRplMQrJ'  # Replace with your folder ID or remove if not needed

    # Specify the directory where your photos are located
    photo_directory = '/home/michael/Pictures/Screenshots'

    # Upload each photo in the directory
    for photo_file in os.listdir(photo_directory):
        photo_path = os.path.join(photo_directory, photo_file)
        if os.path.isfile(photo_path):
            upload_photo(drive_service, photo_path, folder_id)

if __name__ == '__main__':
    main()
