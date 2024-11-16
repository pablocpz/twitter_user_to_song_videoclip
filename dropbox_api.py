# import os
# import dropbox
# import requests
# import configparser
# import random


# class DropboxUploader:
#     def __init__(self):
#         # Configuration parameters
#         self.source_directory = ""
#         self.local_file_path = f'{random.random()}-downloaded_song{random.randint(0,10)}.mp3'
#         self.credentials_directory = "credentials.ini"
#         self.dropbox_directory = "/audiogen-bucket"

#         # Initialize Dropbox API with access token
#         self.access_token = self.read_credentials_value("Authentication", "access_token")
#         self.dbx = dropbox.Dropbox(self.access_token)

#     def read_credentials_value(self, section, key):
#         # Read a value from the credentials file
#         config = configparser.ConfigParser()
#         config.read(self.credentials_directory)

#         try:
#             return config.get(section, key)
#         except (configparser.NoSectionError, configparser.NoOptionError) as e:
#             print(f"read_credentials_value function: Error reading config value: {e}")
#             return None

#     def update_credentials_key_value(self, section, key, value):
#         # Update a key-value pair in the credentials file
#         config = configparser.ConfigParser()
#         config.read(self.credentials_directory)
#         config.set(section, key, value)

#         with open(self.credentials_directory, 'w') as config_file:
#             config.write(config_file)
#             print(f"Key '{key}' value updated successfully in section '{section}'")

#     def generate_new_access_token(self, app_key, app_secret, refresh_token):
#         # Generate a new access token using the provided credentials
#         url = "https://api.dropbox.com/oauth2/token"
#         headers = {"Content-Type": "application/x-www-form-urlencoded"}
#         data = {
#             "grant_type": "refresh_token",
#             "refresh_token": refresh_token,
#             "client_id": app_key,
#             "client_secret": app_secret,
#         }

#         response = requests.post(url, headers=headers, data=data)

#         if response.status_code == 200:
#             return response.json().get("access_token")
#         else:
#             print("generate_new_access_token function: Failed to get a new access token.")
#             print(f"generate_new_access_token function: Status code: {response.status_code}")
#             print(f"generate_new_access_token function: Response: {response.text}")
#             return None

#     def check_token_validity(self):
#         # Check if the existing token is still valid
#         try: 
#             self.dbx.files_list_folder('')
#             print("Token is valid")
#         except dropbox.exceptions.AuthError:
#             print("Token is expired, generating new access token ...")
#             app_key = self.read_credentials_value("Authentication", "app_key")
#             app_secret = self.read_credentials_value("Authentication", "app_secret")
#             refresh_token = self.read_credentials_value("Authentication", "refresh_token")
#             new_token = self.generate_new_access_token(app_key, app_secret, refresh_token)

#             if new_token:
#                 self.update_credentials_key_value("Authentication", "access_token", new_token)
#                 self.access_token = new_token
#                 self.dbx = dropbox.Dropbox(self.access_token)
#         except dropbox.exceptions.DropboxException as e:
#             print("check_token_validity function: An error occurred while checking the token:", e)

#     def upload_files(self):
#         # Upload a file to Dropbox
#         try:
#             self.check_token_validity()
#             file_name = os.path.basename(self.local_file_path)

#             print(f"- Uploading to: {self.dropbox_directory}/{file_name}")

#             with open(self.local_file_path, "rb") as file:
#                 self.dbx.files_upload(file.read(), f"{self.dropbox_directory}/{file_name}", mode=dropbox.files.WriteMode("overwrite"))
#                 print(f"File '{file_name}' uploaded successfully to Dropbox.")

#         except Exception as e:
#             print("upload_files function: An error occurred:", e)

#     def list_folder_paths(self, dropbox_folder=None):
#         """List all file paths in a Dropbox folder."""
#         try:
#             folder_to_list = dropbox_folder if dropbox_folder else self.dropbox_directory
#             result = self.dbx.files_list_folder(folder_to_list)

#             print(f"Listing contents of folder: {folder_to_list}")

#             # Recorre los resultados y muestra el path relativo
#             for entry in result.entries:
#                 print(f"Path relativo: {entry.path_lower}")

#         except dropbox.exceptions.ApiError as err:
#             print(f"Error listando la carpeta: {err}")

#     def get_shared_link(self, file_path):
#         """Get a shared link for a file in Dropbox."""
#         try:
#             shared_link_metadata = self.dbx.sharing_create_shared_link_with_settings(file_path)
#             # Imprime la URL de compartir
#             print(f"URL de compartir: {shared_link_metadata.url}")
            
#             return shared_link_metadata
#         except dropbox.exceptions.ApiError as err:
#             print(f"Error obteniendo el enlace para compartir: {err}")

# def run():
#     # Main program flow
#     print("Start uploading and sharing file ...")
#     dropbox_uploader = DropboxUploader()
    
#     # Sube el archivo
#     dropbox_uploader.upload_files()

#     # Genera el path completo del archivo subido
#     file_path = f"{dropbox_uploader.dropbox_directory}/{os.path.basename(dropbox_uploader.local_file_path)}"

#     # Obtén y muestra la URL pública para compartir
#     link = dropbox_uploader.get_shared_link(file_path)
#     print("End of file upload and sharing.")
    
#     return link



import os
import dropbox
import requests
import configparser
import random

class DropboxUploader:
    def __init__(self):
        # Configuration parameters
        self.local_file_path = f'{random.random()}-downloaded_song{random.randint(0,10)}.mp3'
        self.credentials_directory = "credentials.ini"
        self.dropbox_directory = "/audiogen-bucket"

        # Initialize Dropbox API with access token
        self.access_token = self.read_credentials_value("Authentication", "access_token")
        self.dbx = dropbox.Dropbox(self.access_token)

    def read_credentials_value(self, section, key):
        # Read a value from the credentials file
        config = configparser.ConfigParser()
        config.read(self.credentials_directory)

        try:
            return config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            print(f"read_credentials_value function: Error reading config value: {e}")
            return None

    def update_credentials_key_value(self, section, key, value):
        # Update a key-value pair in the credentials file
        config = configparser.ConfigParser()
        config.read(self.credentials_directory)
        config.set(section, key, value)

        with open(self.credentials_directory, 'w') as config_file:
            config.write(config_file)
            print(f"Key '{key}' value updated successfully in section '{section}'")

    def generate_new_access_token(self, app_key, app_secret, refresh_token):
        # Generate a new access token using the provided credentials
        url = "https://api.dropbox.com/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": app_key,
            "client_secret": app_secret,
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print("generate_new_access_token function: Failed to get a new access token.")
            print(f"generate_new_access_token function: Status code: {response.status_code}")
            print(f"generate_new_access_token function: Response: {response.text}")
            return None

    def check_token_validity(self):
        # Check if the existing token is still valid
        try: 
            self.dbx.files_list_folder('')
            print("Token is valid")
        except dropbox.exceptions.AuthError:
            print("Token is expired, generating new access token ...")
            app_key = self.read_credentials_value("Authentication", "app_key")
            app_secret = self.read_credentials_value("Authentication", "app_secret")
            refresh_token = self.read_credentials_value("Authentication", "refresh_token")
            new_token = self.generate_new_access_token(app_key, app_secret, refresh_token)

            if new_token:
                self.update_credentials_key_value("Authentication", "access_token", new_token)
                self.access_token = new_token
                self.dbx = dropbox.Dropbox(self.access_token)
        except dropbox.exceptions.DropboxException as e:
            print("check_token_validity function: An error occurred while checking the token:", e)

    def download_file(self, url):
        # Download the MP3 file from a public URL
        try:
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                with open(self.local_file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"File downloaded successfully from {url}")
            else:
                print(f"Failed to download file from {url}, status code: {response.status_code}")

        except Exception as e:
            print(f"download_file function: Error downloading file: {e}")

    def upload_files(self):
        # Upload the downloaded file to Dropbox
        try:
            self.check_token_validity()
            file_name = os.path.basename(self.local_file_path)

            print(f"- Uploading to: {self.dropbox_directory}/{file_name}")

            with open(self.local_file_path, "rb") as file:
                self.dbx.files_upload(file.read(), f"{self.dropbox_directory}/{file_name}", mode=dropbox.files.WriteMode("overwrite"))
                print(f"File '{file_name}' uploaded successfully to Dropbox.")
        except Exception as e:
            print(f"upload_files function: An error occurred: {e}")

    def get_shared_link(self, file_path):
        # Get a shared link for a file in Dropbox
        try:
            shared_link_metadata = self.dbx.sharing_create_shared_link_with_settings(file_path)
            print(f"URL de compartir: {shared_link_metadata.url}")
            return shared_link_metadata.url
        except dropbox.exceptions.ApiError as err:
            print(f"Error obteniendo el enlace para compartir: {err}")

def run(suno_url):
    # Example URL to download an MP3 file (replace this with the actual public link)
    # mp3_url = "https://example.com/sample.mp3"

    print("Start downloading and uploading file ...")
    dropbox_uploader = DropboxUploader()
    
    # Download the file from the provided URL
    dropbox_uploader.download_file(suno_url)

    # Upload the downloaded file to Dropbox
    dropbox_uploader.upload_files()

    # Generate the full file path for the uploaded file
    file_path = f"{dropbox_uploader.dropbox_directory}/{os.path.basename(dropbox_uploader.local_file_path)}"

    # Get and print the public sharing URL for the uploaded file
    link = dropbox_uploader.get_shared_link(file_path)
    print("End of file download, upload, and sharing.")

    return link
