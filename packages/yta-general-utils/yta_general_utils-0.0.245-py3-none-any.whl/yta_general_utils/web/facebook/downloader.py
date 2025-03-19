
from yta_general_utils.web.scraper.chrome_scraper import ChromeScraper
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.programming.output import Output
from yta_general_utils.downloader.utils import get_file
from yta_general_utils.dataclasses import FileReturn
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from typing import Union
from io import BytesIO


def download_facebook_video(
    url: str,
    output_filename: Union[str, None, bool] = None
) -> Union[FileReturn, BytesIO]:
    """
    Gets the Facebook video (reel) from the provided 'url' (if valid)
    and returns its data or stores it locally as 'output_filename' if
    provided.
    """
    DOWNLOAD_FACEBOOK_VIDEO_URL = 'https://fdownloader.net/en/facebook-reels-downloader'

    scraper = ChromeScraper()
    scraper.go_to_web_and_wait_until_loaded(DOWNLOAD_FACEBOOK_VIDEO_URL)

    # We need to wait until video is shown
    url_input = scraper.find_element_by_id('s_input')
    url_input.send_keys(url)
    url_input.send_keys(Keys.ENTER)

    # We need to click in the upper left image to activate vid popup
    image_container = scraper.find_element_by_class_waiting('div', 'image-fb open-popup')
    image = image_container.find_element(By.TAG_NAME, 'img')
    image.click()

    #video_element = scraper.find_element_by_element_type_waiting('video')
    video_element = scraper.find_element_by_id_waiting('vid')
    video_source_url = video_element.get_attribute('src')

    if output_filename is False:
        return BytesIO(get_file(video_source_url, None))
    
    output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)
    video = get_file(video_source_url, output_filename)

    return FileReturn(
        video,
        output_filename
    )