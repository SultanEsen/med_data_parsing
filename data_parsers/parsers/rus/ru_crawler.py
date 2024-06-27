import logging
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from parsers.base import SeleniumCrawler

logger = logging.getLogger(__name__)


class RuCrawler(SeleniumCrawler):
    MAIN_URL = "https://grls.rosminzdrav.ru/LimPriceArchive.aspx"
    BASE_URL = "https://grls.rosminzdrav.ru"
    DOCUMENTS_DIRECTORY = "rus"

    def __init__(self, url: str, download_dir: Path):
        """
        Parameters:
            url: url to download
            download_dir: path to download directory within GENERAL_DOCUMENTS_DIRECTORY
        """
        super().__init__(url, download_dir)
        logging.info(f"Loading {url} for Rus crawler")
        self.url = url
        self.download_dir = download_dir

    def get_page(self, url=""):
        if not url:
            url = self.url
        self.driver.get(self.url)

    def find_date_link(self):
        # links = self.driver.find_elements(By.CSS_SELECTOR, "table.ts1 td a")
        # links[-1].click()
        links = WebDriverWait(self.driver, 25).until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[@class="ts1"]//td/a'))
        )
        links[-1].click()

    def find_latest_document(self) -> str:
        # link = self.driver.find_element(By.XPATH, '//table[@class="ts1"]/tbody/tr/td/a')
        # return link.get_attribute("href")
        link = WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.XPATH, '//table[@class="ts1"]/tbody/tr/td/a'))
        )
        return link.get_attribute("href")
