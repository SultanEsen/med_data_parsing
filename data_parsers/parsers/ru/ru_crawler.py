import requests
from parsel import Selector
from datetime import datetime
import logging

from parsers.base import Crawler


logger = logging.getLogger(__name__)


class RuCrawler(Crawler):
    MAIN_URL = "https://grls.rosminzdrav.ru/LimPriceArchive.aspx"
    BASE_URL = "https://grls.rosminzdrav.ru"
    DOCUMENTS_DIRECTORY = "rus"

    def __init__(self, url):
        super().__init__(url)
        logging.info(f"Loading {url} for Rus crawler")
        self.url = url

    def get_page(self, url=''):
        if not url:
            url = self.url
        response = self.session.get(self.url)
        return response.text

    def find_date_link(self, text):
        html = Selector(text)
        # table = html.css("table.ts1 tbody td a")
        table = html.css("table.ts1").css("td").css("a")
        if not len(table):
            logging.info("Table not found")
            return
        last_cell = table[-1].attrib["href"]
        logger.info(f"Last cell: {last_cell}")
        return last_cell

    def find_latest_document(self, text):
        html = Selector(text)
        nodes = html.css("td").css("a")
        logging.info(f"Found {len(nodes)} links")
        if nodes and len(nodes) > 0:
            return nodes[-1].attrib["href"]

    def load_document(self, url=''):
        if self.BASE_URL.replace("https://", "") not in url:
            url = self.BASE_URL + url
        logging.info(f"Loading {url}")
        try:
            response = self.session.get(url)
        except requests.exceptions.HTTPError:
            logging.error(f"Failed to download {url} due to HTTP error")
        except requests.exceptions.ConnectionError:
            logging.error(f"Failed to download {url} due to connection error")
        else:
            if response.status_code == 200:
                logging.info("Loading ...")
                file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                file_path = f"{self.GENERAL_DOCUMENTS_DIRECTORY}/{self.DOCUMENTS_DIRECTORY}/{file_name}.pdf"
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                logging.info(f"Saved to {file_path}")
                return file_path
