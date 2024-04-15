import logging
from datetime import datetime
from pathlib import Path

from parsers.uzb.uzb import UZBCrawler
from parsers.uzb.uzb_pdf import UZBFileParser
from parsers.uzb.repository import DocumentRepo, DataRepo
from utils import get_latest_files


class UZBService:
    def __init__(self, session):
        self.crawler = UZBCrawler(UZBCrawler.MAIN_URL)
        self.parser = UZBFileParser()
        self.repo = DocumentRepo(session)
        self.data_repo = DataRepo(session)
        self.tables = ()
        self.file = ''

    async def download_file(self):
        for text in self.crawler.get_initial_page():
            logging.info("Searching ...")
            urls = self.crawler.find_latest_document(text)
            logging.info(f"Found {urls}")
            if urls:
                item = await self.repo.get(urls)
                if not item:
                    logging.info("Downloading file ...")
                    self.crawler.load_document(urls)
                    await self.repo.add(urls)

    def parse_data(self):
        file = get_latest_files(UZBCrawler.DOCUMENTS_DIRECTORY)
        if file:
            file_path = Path(
                UZBCrawler.GENERAL_DOCUMENTS_DIRECTORY,
                UZBCrawler.DOCUMENTS_DIRECTORY,
                file
            )
            self.file = file_path
            self.tables = self.parser.read_file(file_path)

    async def save_data(self):
        for ind, table in enumerate(self.tables):
            if ind > 2:
                continue
            assert table.shape[1] == 11, f"Number of columns in file {self.file} is incorrect"
            await self.data_repo.add(table)

    async def parse(self):
        # await self.download_file()
        self.parse_data()
        await self.save_data()
