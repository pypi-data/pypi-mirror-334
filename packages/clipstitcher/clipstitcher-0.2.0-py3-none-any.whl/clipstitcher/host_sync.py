from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

class Uploader():
    def __init__(self, secrets_path='client_secrets.json'):
        GoogleAuth.DEFAULT_SETTINGS['client_config_file']=secrets_path
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()  # Follow the authentication instructions
        self.drive = GoogleDrive(self.gauth)


    def upload_file(self, file_path, parent_folder_id):

        file_name = os.path.split(file_path)[1]
        q = f"'{parent_folder_id}' in parents and trashed = false and title = '{file_name}'"
        results = self.drive.ListFile({'q': q}).GetList()
        if results:
            existing_file_id = results[0]['id']
            file_metadata = {}
            updated_file = self.drive.CreateFile({'id': existing_file_id})
            updated_file.SetContentFile(file_path)
            updated_file.Upload()
            file_id = existing_file_id
            print(f'Replacing file {file_name}. File ID: {file_id}')
        else:
            file_metadata = {'name': file_name, 'parents': [{'id': parent_folder_id}]}
            new_file = self.drive.CreateFile(file_metadata)
            new_file.SetContentFile(file_path)
            new_file.Upload()
            file_id = new_file.get("id")
            print(f'Creating new {file_name}. File ID: {file_id}')
        return file_id
