from yta_general_utils.programming.path import get_project_abspath
from yta_google_api.oauth.google_oauth_api import GoogleOauthAPI


API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']
CLIENT_SECRET_FILENAME = get_project_abspath() + 'client-secret.json'
TOKEN_FILES_ABSPATH = get_project_abspath() + 'token_files/'

class YoutubeAPI:
    """
    Class to simplify and encapsulate the
    functionality related to the Youtube API
    flow, tokens and credentials handling.
    """

    @staticmethod
    def is_youtube_token_valid() -> bool:
        """
        Check if the current Youtube Data v3 API
        token is valid or not.
        """
        return GoogleOauthAPI(CLIENT_SECRET_FILENAME, TOKEN_FILES_ABSPATH).is_oauth_token_valid(API_NAME, API_VERSION, SCOPES)

    @staticmethod
    def start_youtube_auth_flow():
        """
        Start the Google Auth flow for Youtube Data
        v3 API.
        """
        return GoogleOauthAPI(CLIENT_SECRET_FILENAME, TOKEN_FILES_ABSPATH).start_google_auth_flow(API_NAME, API_VERSION, SCOPES)

    @staticmethod
    def create_youtube_service():
        """
        Create a Youtube Data v3 API service and
        return it.
        """
        return GoogleOauthAPI(CLIENT_SECRET_FILENAME, TOKEN_FILES_ABSPATH).create_service(API_NAME, API_VERSION, SCOPES)
