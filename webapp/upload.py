from google.oauth2 import service_account
from googleapiclient.discovery import build, MediaFileUpload
from googleapiclient.http import MediaIoBaseUpload
import io
import socket

def get_creds():
	SCOPES = ['https://www.googleapis.com/auth/drive']
	hostname = socket.gethostname()
	if hostname == "DESKTOP-MG5V3KN":
		SERVICE_ACCOUNT_FILE = 'C:/Users/mattl/OneDrive/005_Env-Files/cherry-pi website/project-cherry-pi-28156479eae6.json'
	elif hostname == "vps6084.first-root.com":
		SERVICE_ACCOUNT_FILE = '/var/www/cherry-pi-prod/project-cherry-pi-28156479eae6.json'
	else:
		raise FileNotFoundError("drive api filepath not specified")


	credentials = service_account.Credentials.from_service_account_file(
			SERVICE_ACCOUNT_FILE, scopes=SCOPES)

	return credentials

def upload_file(file_object, file_data, credentials, path=False):
	service = build('drive', 'v3', credentials=credentials)

	# print(file_object)

	folder_metadata = {
		'name': 'My Test Folder',
		'mimeType': 'application/vnd.google-apps.folder'
	}
	cloudFolder = service.files().create(body=folder_metadata).execute()

	file_metadata = {
		'name': file_data["file_name"],
		'parents': [cloudFolder['id']]
	}
	try:
		if path:
			media = MediaFileUpload(file_object, mimetype=file_data["mimetype"], resumable=True)
		else:
			media = MediaIoBaseUpload(io.BytesIO(file_object), mimetype=file_data["mimetype"], resumable=True)
		cloudFile = service.files().create(body=file_metadata, media_body=media).execute()
		# print(cloudFile)
		file_id = cloudFile['id']
		userEmail = "mattl1598@gmail.com"
		cloudPermissions = service.permissions().create(fileId=cloudFile['id'], body={'type': 'user', 'role': 'reader', 'emailAddress': userEmail}).execute()
		cp = service.permissions().list(fileId=cloudFile['id']).execute()
		# print(cp)
	except Exception as e:
		print(e)
		file_id = None

	return file_id


def getFileSize(id):
	service = build('drive', 'v3', credentials=get_creds())

	return service.files().get(fileId=id, fields='size').execute()


# print(getFileSize(None))