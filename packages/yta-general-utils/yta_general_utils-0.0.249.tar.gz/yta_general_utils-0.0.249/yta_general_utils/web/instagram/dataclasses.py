from dataclasses import dataclass


@dataclass
class InstagramUrl:

    video_id: str
    """
    The id of the video.
    """
    url: str
    """
    The short Instagram url of that video.
    """

    def __init__(
        self,
        video_id: str,
        url: str
    ):
        self.video_id = video_id
        self.url = url