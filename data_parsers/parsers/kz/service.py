from parsers.base import Crawler
from parsel import Selector
import requests
from datetime import datetime
import logging


class KAZCrawler(Crawler):
    MAIN_URL = "https://pharmnewskz.com/ru/legislation/prikaz-mz-rk-ot-7-avgusta-2023-goda--465_7459"
    BASE_URL = "https://pharmnewskz.com"
    DOCUMENTS_DIRECTORY = "kaz"

    def __init__(self, url):
        super().__init__(url)
        logging.info(f"Loading {url} for KAZ crawler")
        self.url = url

    def get_initial_page(self):
        response = self.session.get(self.url)
        yield response.text

    def find_document_link(self, text):
        html = Selector(text)
        nodes = html.css("a.loadDoc")
        logging.info(f"Found {len(nodes)} links")
        if nodes and len(nodes) > 0:
            full_path = self.BASE_URL + nodes[-1].attrib["href"]
            logging.info(f"Full path: {full_path}")
            return full_path

    def load_document(self, url=''):
        logging.info(f"Loading {url}")
        try:
            response = self.session.get(url)
        except requests.exceptions.HTTPError:
            logging.error(f"Failed to download {url} due to HTTP error")
        else:
            if response.status_code == 200:
                logging.info("Loading ...")
                file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                file_path = f"{self.GENERAL_DOCUMENTS_DIRECTORY}/{self.DOCUMENTS_DIRECTORY}/{file_name}.docx"
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                logging.info(f"Saved to {file_path}")
                return file_path


class KAZService:
    def __init__(self):
        self.crawler = KAZCrawler(KAZCrawler.MAIN_URL)
        self.file = ''

    async def download_file(self):
        for text in self.crawler.get_initial_page():
            logging.info("Searching ...")
            urls = self.crawler.find_document_link(text)
            logging.info(f"Found {urls}")
            if urls:
                self.crawler.load_document(urls)

    async def parse(self):
        await self.download_file()
