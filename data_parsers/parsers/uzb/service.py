import logging
from datetime import datetime
from pathlib import Path
from pprint import pprint
import pandas as pd

from parsers.uzb.uzb import UZBCrawler
from parsers.uzb.uzb_pdf import UZBFileParser
from parsers.uzb.repository import DocumentRepo, DataRepo
from utils import get_latest_files


logger = logging.getLogger(__name__)


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
            logger.info("Searching ...")
            urls = self.crawler.find_latest_document(text)
            # logger.info(f"Found {urls}")
            if urls:
                item = await self.repo.get(urls)
                if not item:
                    logger.info("Downloading file ...")
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
            file = self.parser.read_file(file_path)
            for ind, page in enumerate(file):
                if ind == 0:
                    self.headings = page[0][0]
                    data = page[0][1:]
                else:
                    data = page[0]
                # if ind > 10:
                #     break
                yield pd.DataFrame(data, columns=self.headings), ind
                logger.info(f"processed page number {ind+1}")

    async def save_data(self):
        for df, ind in self.parse_data():
            # logger.info(f"Found {df.shape[1]} columns")
            assert df.shape[1] == 11, f"Number of columns in file {self.file} is incorrect,\
                shoud be 11 but now is {df.shape[1]}, table number is {ind+1}"
            df[['МНН', 'Упаковка ЛП']].apply(lambda x: x.str.replace("\n", " ").str.strip())
            await self.data_repo.add(df)
            del df

    async def parse(self):
        # await self.download_file()
        # self.parse_data()
        # await self.save_data()
        pass
