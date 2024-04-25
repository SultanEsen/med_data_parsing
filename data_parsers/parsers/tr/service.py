import logging
from datetime import datetime
from pathlib import Path
from pprint import pprint

from parsers.tr.turk import TURKCrawler
from parsers.tr.turk_xlsx import TURKFileParser
from parsers.tr.repository import DocumentRepo, DataRepo
from utils import get_latest_files


class TURKService:
    def __init__(self, session):
        self.crawler = TURKCrawler(TURKCrawler.MAIN_URL)
        self.parser = TURKFileParser()
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
        file = get_latest_files(TURKCrawler.DOCUMENTS_DIRECTORY)
        if file:
            file_path = Path(
                TURKCrawler.GENERAL_DOCUMENTS_DIRECTORY,
                TURKCrawler.DOCUMENTS_DIRECTORY,
                file
            )
            self.file = file_path
            self.tables = self.parser.read_file(file_path)

    async def save_data(self):
        pprint(self.tables) 
        print(type(self.tables))
        # for ind, table in enumerate(self.tables):
        #     if ind > 2:
        #         continue
        assert self.tables.shape[1] == 3, f"Number of columns in file {self.file} is incorrect"
        await self.data_repo.add(self.tables)

    async def parse(self):
        # await self.download_file()
        self.parse_data()
        await self.save_data()
