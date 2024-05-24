from parsers.base import Crawler
from parsel import Selector
import requests
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class MoldovaCrawler(Crawler):
    MAIN_URL = ""
    BASE_URL = ""
    DOCUMENTS_DIRECTORY = "mld"

    def __init__(self, url):
        super().__init__(url)
        logger.info(f"Loading {url} for MD crawler")
        self.url = url

    def get_page(self, url=''):
        if not url:
            url = self.url
        response = self.session.get(url)
        return response.text

    def get_initial_page(self):
        pass

    def find_latest_document(self, text):
        pass

    def load_document(self, url):
        pass
