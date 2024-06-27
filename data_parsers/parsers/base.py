import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import time

class Crawler:
    GENERAL_DOCUMENTS_DIRECTORY = "documents"

    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
        }


class SeleniumCrawler:
    GENERAL_DOCUMENTS_DIRECTORY = "documents"

    def __init__(self, url: str, download_dir: Path):
        self.url = url
        self.download_dir = download_dir
        if not Path(self.download_dir).exists():
            Path(self.download_dir).mkdir(parents=True)
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": str(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        self.driver = None
        self.options = chrome_options

    def start(self):
        self.driver = webdriver.Chrome(options=self.options)

    def wait_for_download(self, timeout=60):
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < timeout:
            time.sleep(1)
            for f in Path(self.download_dir).iterdir():
                if f.file_name.endswith(".crdownload"):
                    dl_wait = True
                    break
                else:
                    dl_wait = False
            seconds += 1

        return dl_wait