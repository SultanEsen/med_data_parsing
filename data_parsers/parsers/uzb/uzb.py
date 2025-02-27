import requests
from parsel import Selector
from datetime import datetime
import logging

from parsers.base import Crawler


logger = logging.getLogger(__name__)


class UZBCrawler(Crawler):
    MAIN_URL = "https://uzpharmagency.uz/ru/menu/referentnye-tseny"
    BASE_URL = "https://uzpharmagency.uz"
    DOCUMENTS_DIRECTORY = "uzb"

    def __init__(self, url):
        super().__init__(url)
        logger.info(f"Loading {url} for UZB crawler")
        self.url = url

    def get_initial_page(self):
        response = self.session.get(self.url)
        yield response.text

    def find_latest_document(self, text):
        html = Selector(text)
        nodes = html.css("td").css("a")
        logger.info(f"Found {len(nodes)} links")
        if nodes and len(nodes) > 0:
            return nodes[-1].attrib["href"]

    def load_document(self, url=''):
        if self.BASE_URL.replace("https://", "") not in url:
            url = self.BASE_URL + url
        logger.info(f"Loading {url}")
        try:
            response = self.session.get(url)
        except requests.exceptions.HTTPError:
            logger.error(f"Failed to download {url} due to HTTP error")
        except requests.exceptions.ConnectionError:
            logger.error(f"Failed to download {url} due to connection error")
        else:
            if response.status_code == 200:
                logger.info("Loading ...")
                file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                file_path = f"{self.GENERAL_DOCUMENTS_DIRECTORY}/{self.DOCUMENTS_DIRECTORY}/{file_name}.pdf"
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                logger.info(f"Saved to {file_path}")
                return file_path
