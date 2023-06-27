import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the scope of access required
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    # Check if the credentials pickle file exists
    creds_filename = 'credentials.pickle'
    creds = None
    if os.path.exists(creds_filename):
        with open(creds_filename, 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no valid credentials available, ask the user to authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(creds_filename, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def upload_photo(service, file_path):
    # Set the file metadata
    file_metadata = {'name': os.path.basename(file_path)}
    
    # Create the media object for uploading
    media = MediaFileUpload(file_path, resumable=True)
    
    # Upload the file to Google Drive
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    print(f'Successfully uploaded {file_path} with ID: {file["id"]}')

def main():
    # Authenticate the user and get the credentials
    creds = authenticate()
    
    # Build the Drive API service
    service = build('drive', 'v3', credentials=creds)
    
    # Specify the directory containing the photos
    photo_directory = '/path/to/photo/directory'
    
    # Upload each photo in the directory
    for filename in os.listdir(photo_directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            file_path = os.path.join(photo_directory, filename)
            upload_photo(service, file_path)

if __name__
