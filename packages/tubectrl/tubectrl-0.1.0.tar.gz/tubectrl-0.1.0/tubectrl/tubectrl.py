from gverify import GoogleOAuth, YouTubeScopes
from pydantic import BaseModel
from typing import Any, Optional
from .exceptions import MissingClientSecretsFile, InvalidSecretsFileError
from pathlib import Path
from gverify import InvalidSecretsFileException
from .models import Video
from .resources import YouTubeVideoResource


class YouTube(BaseModel):
    """Provides methods for interacting with the YouTube API.

    This class acts as an interface to the YouTube API, providing methods for interacting with
    the YouTube V3 API.

    Attributes
    ----------
    client_secret_file: str
        The path to the json file containing your authentication information.
    """

    client_secret_file: Optional[str] = None
    youtube_client: Optional[Any] = None

    def authenticate(self, client_secret_file: Optional[str] = None) -> None:
        """Authenticate the requests made to youtube.

        Used to generate the credentials that are used when authenticating requests to youtube.

        Parameters
        ----------
        client_secret_file: str
            The path to clients secret json file from Google

        Raises
        ------
        ValueError:
            When the client secrets file is not provided
        FileNotFoundError:
            When the secrets file path is not found
        """
        if client_secret_file:
            self.client_secret_file = client_secret_file
        if not self.client_secret_file:
            raise MissingClientSecretsFile("The client secret file must be provided.")
        if not Path(self.client_secret_file).exists():
            raise FileNotFoundError("The client secret file was not found.")
        api_service_name: str = "youtube"
        api_version: str = "v3"
        credentials_dir: str = ".youtube"
        scopes: list[str] = [
            YouTubeScopes.youtube.value,
            YouTubeScopes.youtube_force_ssl.value,
            YouTubeScopes.youtube_upload.value,
        ]
        oauth: GoogleOAuth = GoogleOAuth(
            secrets_file=self.client_secret_file,
            scopes=scopes,
            api_service_name=api_service_name,
            api_version=api_version,
            credentials_dir=credentials_dir,
        )
        try:
            self.youtube_client = oauth.authenticate_google_server()
        except InvalidSecretsFileException as e:
            raise InvalidSecretsFileError(e)

    def find_video_by_id(self, video_id: str) -> Video:
        """Find a single video by providing the video's id.

        Parameters
        ----------
        video_id: str
            The video's id
        Returns
        -------
        Video:
            A Video instance
        """
        if not video_id:
            raise ValueError("The video id was not provided")
        video_resource: YouTubeVideoResource = YouTubeVideoResource(
            youtube_client=self.youtube_client
        )
        video: Video = video_resource.find_video_by_id(video_id=video_id)
        return video

    def find_videos_by_ids(self, video_ids: list[str]) -> list[Video]:
        """Find a many videos by providing a list of video ids.

        Parameters
        ----------
        video_ids: list[str]
            A list of video ids
        Returns
        -------
        list[Video]:
            A list of Video instances
        """
        if not video_ids:
            raise ValueError("The video id was not provided")
        video_resource: YouTubeVideoResource = YouTubeVideoResource(
            youtube_client=self.youtube_client
        )
        videos: list[Video] = video_resource.find_videos_by_ids(video_ids=video_ids)
        return videos
