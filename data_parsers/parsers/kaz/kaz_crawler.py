from parsers.base import Crawler
from parsel import Selector
import requests
from datetime import datetime
import logging


class KazCrawler(Crawler):
    MAIN_URL = "https://www.ndda.kz/category/cena"
    BASE_URL = "https://www.ndda.kz"
    DOCUMENTS_DIRECTORY = "kaz"

    def __init__(self, url):
        super().__init__(url)
        logging.info(f"Loading {url} for KAZ crawler")
        self.url = url

    def get_page(self, url=''):
        if not url:
            url = self.url
        response = self.session.get(url)
        return response.text

    def find_iframe_link(self, text):
        html = Selector(text)
        iframe_src = html.xpath("//iframe/@src").get()
        if iframe_src:
            full_path = self.BASE_URL + iframe_src
            page = self.get_page(full_path)
            return page

    def find_document_link(self, text):
        html = Selector(text)
        document_url = html.xpath("//div[@ng-controller='appController']//a/@href").get()
        if document_url:
            full_path = self.BASE_URL + document_url
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
                file_path = f"{self.GENERAL_DOCUMENTS_DIRECTORY}/{self.DOCUMENTS_DIRECTORY}/{file_name}.pdf"
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                logging.info(f"Saved to {file_path}")
                return file_path

