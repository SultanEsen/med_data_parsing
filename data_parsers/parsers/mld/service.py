import logging
from datetime import datetime
from pathlib import Path
from pprint import pprint
import logging

from parsers.mld.mld_crawler import MoldovaCrawler
from parsers.mld.mld_parser import MoldovaFileParser
from parsers.repository import DocumentRepo
from parsers.mld.repository import DataRepo
from utils import get_latest_files


logger = logging.getLogger(__name__)


class MoldovaService:
    def __init__(self, session):
        self.crawler = MoldovaCrawler(MoldovaCrawler.MAIN_URL)
        self.parser = MoldovaFileParser()
        self.repo = DocumentRepo(session)
        self.data_repo = DataRepo(session)
        self.tables = ()
        self.file = ''
        self.headers = ()

    async def download_file(self):
        # TODO: Implement downloading
        for text in self.crawler.get_initial_page():
            logging.info("Searching ...")
            urls = self.crawler.find_latest_document(text)
            logging.info(f"Found {urls}")
            if urls:
                item = await self.repo.get(urls)
                if not item:
                    logging.info("Downloading file ...")
                    self.crawler.load_document(urls)
                    await self.repo.add(url=urls, country='Moldova')

    def parse_data(self):
        file = get_latest_files(MoldovaCrawler.DOCUMENTS_DIRECTORY)
        if file:
            file_path = Path(
                MoldovaCrawler.GENERAL_DOCUMENTS_DIRECTORY,
                MoldovaCrawler.DOCUMENTS_DIRECTORY,
                file
            )
            self.file = file_path
            self.tables = self.parser.read_file(file_path)
            self.headers = self.tables.head()
            logger.info(self.tables.iloc[0, :].to_list())
            self.tables = self.tables.iloc[1:, :]
            # self.tables.columns = self.headers

    def divide_into_chunks(self, df, n):
        # looping till length of data
        for i in range(0, len(df), n):
            yield df.iloc[i:i + n]

    def process_columns(self, df):
        pass

    async def save_data(self):
        if len(self.tables) and len(self.headers):
            self.process_columns(self.tables)
            logger.info(self.headers)
            # for ind, chunk in enumerate(self.divide_into_chunks(self.tables, 100)):
            #     logger.info(f"Saving chunk {ind}")
            #     await self.data_repo.add(chunk)

    async def parse(self):
        # await self.download_file()
        self.parse_data()
        await self.save_data()
