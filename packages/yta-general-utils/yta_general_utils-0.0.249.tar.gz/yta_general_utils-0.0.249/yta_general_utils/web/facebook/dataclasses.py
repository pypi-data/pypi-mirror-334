from dataclasses import dataclass


@dataclass
class FacebookUrl:

    video_id: str
    """
    The id of the video.
    """
    url: str
    """
    The short Facebook url of that video.
    """

    def __init__(
        self,
        video_id: str,
        url: str
    ):
        self.video_id = video_id
        self.url = url