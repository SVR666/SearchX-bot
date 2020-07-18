import os
import pickle

import requests
import logging

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from telegram import InlineKeyboardMarkup
from bot.helper.telegram_helper import button_builder
from bot import DRIVE_ID, INDEX_URL, telegra_ph

LOGGER = logging.getLogger(__name__)
logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

class GoogleDriveHelper:
    def __init__(self, name=None, listener=None):
        self.__G_DRIVE_TOKEN_FILE = "token.pickle"
        # Check https://developers.google.com/drive/scopes for all available scopes
        self.__OAUTH_SCOPE = ['https://www.googleapis.com/auth/drive']
        self.__service = self.authorize()

    def get_readable_file_size(self,size_in_bytes) -> str:
        if size_in_bytes is None:
            return '0B'
        index = 0
        size_in_bytes = int(size_in_bytes)
        while size_in_bytes >= 1024:
            size_in_bytes /= 1024
            index += 1
        try:
            return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
        except IndexError:
            return 'File too large'

    def authorize(self):
        # Get credentials
        credentials = None
        if os.path.exists(self.__G_DRIVE_TOKEN_FILE):
            with open(self.__G_DRIVE_TOKEN_FILE, 'rb') as f:
                credentials = pickle.load(f)
        if credentials is None or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.__OAUTH_SCOPE)
                LOGGER.info(flow)
                credentials = flow.run_console(port=0)

            # Save the credentials for the next run
            with open(self.__G_DRIVE_TOKEN_FILE, 'wb') as token:
                pickle.dump(credentials, token)
        return build('drive', 'v3', credentials=credentials, cache_discovery=False)

    def drive_list(self, fileName):
        msg = f'<h4>Search Results for : {fileName}</h4><br>@LoaderXbot #ProjektX<br><br>'
        # Create Search Query for API request.
        INDEX_ID = 0
        for parent_id in DRIVE_ID :
            query = f"'{parent_id}' in parents and (name contains '{fileName}')"
            response = self.__service.files().list(supportsTeamDrives=True,
                                               includeTeamDriveItems=True,
                                               q=query,
                                               spaces='drive',
                                               pageSize=100,
                                               fields='files(id, name, mimeType, size)',
                                               orderBy='modifiedTime desc').execute()
            index_url = INDEX_URL[INDEX_ID]
            INDEX_ID += 1
            msg += f"╾────────────╼<br><b>Team Drive : {INDEX_ID}</b><br>╾────────────╼<br>"
            if response["files"]:
                for file in response.get('files', []):
                    if file.get('mimeType') == "application/vnd.google-apps.folder":  # Detect Whether Current Entity is a Folder or File.
                        msg += f"📁 <code>{file.get('name')}<br>(folder)</code><br>" \
                               f"<b><a href='https://drive.google.com/drive/folders/{file.get('id')}'>Drive Link</a></b>"
                        if index_url is not None:
                            url_path = requests.utils.quote(f'{file.get("name")}')
                            url = f'{index_url}/{url_path}/'
                            msg += f' <b>| <a href="{url}">Index Link</a></b>'

                    else:
                        msg += f"📄 <code>{file.get('name')}<br>({self.get_readable_file_size(file.get('size'))})</code><br>" \
                               f"<b><a href='https://drive.google.com/uc?id={file.get('id')}&export=download'>Drive Link</a></b>"
                        if index_url is not None:
                            url_path = requests.utils.quote(f'{file.get("name")}')
                            url = f'{index_url}/{url_path}'
                            msg += f' <b>| <a href="{url}">Index Link</a></b>'
                    msg += '<br><br>'
            else :
                msg += "⁍ <code>No Results</code><br><br>"
        
        response = telegra_ph.create_page(title = 'LoaderX',
                                            author_name='svr666',
                                            author_url='https://t.me/svr666',
                                            html_content=msg
                                            )['path']

        msg = f"<b>Search Results For {fileName} 👇</b>"
        buttons = button_builder.ButtonMaker()   
        buttons.buildbutton("HERE", f"https://telegra.ph/{response}")

        return msg, InlineKeyboardMarkup(buttons.build_menu(1))
