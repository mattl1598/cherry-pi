from google.oauth2 import service_account
from googleapiclient.discovery import build, MediaFileUpload
from googleapiclient.http import MediaIoBaseUpload
import io

def get_creds():
	SCOPES = ['https://www.googleapis.com/auth/drive']
	SERVICE_ACCOUNT_FILE = 'C:/Users/mattl/OneDrive/005_Env-Files/cherry-pi website/project-cherry-pi-28156479eae6.json'

	credentials = service_account.Credentials.from_service_account_file(
			SERVICE_ACCOUNT_FILE, scopes=SCOPES)

	return credentials

def upload_file(file_object, file_data, credentials):
	service = build('drive', 'v3', credentials=credentials)

	folder_metadata = {
		'name': 'My Test Folder',
		'mimeType': 'application/vnd.google-apps.folder'
	}
	cloudFolder = service.files().create(body=folder_metadata).execute()

	file_metadata = {
		'name': file_data["file_name"],
		'parents': [cloudFolder['id']]
	}

	media = MediaIoBaseUpload(io.BytesIO(file_object), mimetype=file_data["mimetype"], resumable=True)
	cloudFile = service.files().create(body=file_metadata, media_body=media).execute()

	print(cloudFile)

	userEmail = "mattl1598@gmail.com"
	cloudPermissions = service.permissions().create(fileId=cloudFile['id'],
		body={'type': 'user', 'role': 'reader', 'emailAddress': userEmail}).execute()

	cp = service.permissions().list(fileId=cloudFile['id']).execute()
	print(cp)
