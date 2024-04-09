import requests


class Crawler:
    GENERAL_DOCUMENTS_DIRECTORY = "documents"

    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
        }
