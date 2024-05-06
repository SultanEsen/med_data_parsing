import logging
from datetime import datetime
from pathlib import Path

from parsers.ru.ru_crawler import RuCrawler
from parsers.ru.ru_parser import RuFileParser
# from parsers.uzb.repository import DocumentRepo, DataRepo
from utils import get_latest_files


class RuService:
    def __init__(self, session):
        self.crawler = RuCrawler(RuCrawler.MAIN_URL)
        self.parser = RuFileParser()
        # self.repo = DocumentRepo(session)
        # self.data_repo = DataRepo(session)
        self.tables = ()
        self.file = ''

    async def download_file(self):
        initial_page = self.crawler.get_page()
        logging.info("Searching ...")
        link = self.crawler.find_date_link(initial_page)
        return
        urls = self.crawler.find_latest_document(text)
        logging.info(f"Found {urls}")
        if urls:
            # item = await self.repo.get(urls)
            if not item:
                logging.info("Downloading file ...")
                self.crawler.load_document(urls)
                # await self.repo.add(urls)

    def parse_data(self):
        file = get_latest_files(RuCrawler.DOCUMENTS_DIRECTORY)
        if file:
            file_path = Path(
                RuCrawler.GENERAL_DOCUMENTS_DIRECTORY,
                RuCrawler.DOCUMENTS_DIRECTORY,
                file
            )
            self.file = file_path
            self.tables = self.parser.read_file(file_path)

    async def save_data(self):
        # assert table.shape[1] == 11, f"Number of columns in file {self.file} is incorrect"
        await self.data_repo.add(table)

    async def parse(self):
        await self.download_file()
        # self.parse_data()
        # await self.save_data()
