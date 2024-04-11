import logging
from datetime import datetime
from pathlib import Path

from parsers.uzb import UZBCrawler
from parsers.uzb_pdf import UZBFileParser
from parsers.database import DocumentRepo
from utils import get_latest_files


class UZBService:
    def __init__(self, session):
        self.crawler = UZBCrawler(UZBCrawler.MAIN_URL)
        self.parser = UZBFileParser()
        self.repo = DocumentRepo(session)
        self.data_repo = []

    async def download_file(self):
        for text in self.crawler.get_initial_page():
            logging.info("Searching ...")
            urls = self.crawler.find_latest_document(text)
            logging.info(f"Found {urls}")
            if urls:
                item = await self.repo.get(urls)
                if not item:
                    logging.info("Loading ...")
                    self.crawler.load_document(urls)
                    await self.repo.add(urls)

    def parse_data(self):
        file = get_latest_files(UZBCrawler.DOCUMENTS_DIRECTORY)
        if file:
            self.tables = self.parser.read_file(Path(
                UZBCrawler.GENERAL_DOCUMENTS_DIRECTORY,
                UZBCrawler.DOCUMENTS_DIRECTORY,
                file
            ))

    async def save_data(self):
        for table in self.tables:
            await self.repo.add(table)

    async def parse(self):
        await self.download_file()
