import requests
from parsel import Selector
from datetime import datetime
import logging

from parsers.base import Crawler


class TURKCrawler(Crawler):
    MAIN_URL = "https://www.titck.gov.tr/dinamikmodul/100"
    BASE_URL = "https://www.titck.gov.tr"
    DOCUMENTS_DIRECTORY = "turk"

    def __init__(self, url):
        super().__init__(url)
        logging.info(f"Loading {url} for Turkey documents")
        self.url = url

    def get_initial_page(self):
        response = self.session.get(self.url)
        yield response.text

    def find_latest_document(self, text):
        html = Selector(text)
        nodes = html.css("tbody tr td").css("a")
        logging.info(f"Found {len(nodes)} links")
        if nodes and len(nodes) > 0:
            return nodes[0].attrib["href"]

    def load_document(self, url=''):
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
                file_path = f"{self.GENERAL_DOCUMENTS_DIRECTORY}/{self.DOCUMENTS_DIRECTORY}/{file_name}.xlsx"
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                logging.info(f"Saved to {file_path}")
                return file_path
