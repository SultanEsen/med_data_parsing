import requests
from parsel import Selector
from datetime import datetime
import logging

from base import Crawler


class UZBCrawler(Crawler):
    MAIN_URL = "https://uzpharmagency.uz/ru/menu/referentnye-tseny"
    BASE_URL = "https://uzpharmagency.uz"
    DOCUMENTS_DIRECTORY = "uzb"

    def __init__(self, url):
        super().__init__(url)
        self.url = url

    def get_initial_page(self):
        response = self.session.get(self.url)
        yield response.text

    def find_latest_document(self, text):
        html = Selector(text)
        nodes = html.css("td").css("a")
        logging.info(f"Found {len(nodes)} links")
        if nodes and len(nodes) > 0:
            yield nodes[-1].attrib["href"]

    def load_document_1(self, url=UZBCrawler.MAIN_URL):
        if self.BASE_URL not in url:
            url = self.BASE_URL + url
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
                    return file_path

    def load_document(self, url=UZBCrawler.MAIN_URL):
        if self.BASE_URL.replace("https://", "") not in url:
            url = self.BASE_URL + url
        logging.info(f"Loading {url}")
        response = self.session.get(url)
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

    def parse(self):
        for text in self.get_initial_page():
            urls = self.find_latest_document(text)
            logging.info("Searching ...")
            for result in urls:
                logging.info(f"Found {result}")
                if result:
                    return self.load_document(result)


if __name__ == "__main__":
    crawler = UZBCrawler(UZBCrawler.MAIN_URL)
    print(crawler.parse())
