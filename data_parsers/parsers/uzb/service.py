import logging
from datetime import datetime
from pathlib import Path
from pprint import pprint
import pandas as pd

from parsers.uzb.uzb import UZBCrawler
from parsers.uzb.uzb_pdf import UZBFileParser
from parsers.uzb.repository import DataRepo
from parsers.repository import DocumentRepo
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
            if urls:
                item = await self.repo.get(urls)
                if item:
                    logger.info("Downloading file ...")
                    self.crawler.load_document(urls)
                    await self.repo.add(country="uzb", url=urls)

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
                    self.headings[0] = 'ИД упаковки'
                    self.headings[7] = 'Предельная цена'
                    data = page[0][1:]
                else:
                    data = page[0]
                yield pd.DataFrame(data, columns=self.headings), ind

    def process_columns(self, df, ind):
        # logger.info(f"Processing table {df.columns}")
        # df['ИД упаковки'] = df['ИД упаковки'].astype('int64')
        df['ИД упаковки'] = df['ИД упаковки'].str.replace(" ", "")
        df['Валюта'] = df['Валюта'].astype('category')
        df['Предельная цена'] = df['Предельная цена'].str.replace(",", ".")
        df['Предельная цена'] = df['Предельная цена'].str.replace(" ", "")
        df['Предельная цена'] = df['Предельная цена'].fillna(0).astype('float')
        df['Оптовая цена'] = df['Оптовая цена'].str.replace(",", ".")
        df['Оптовая цена'] = df['Оптовая цена'].str.replace(" ", "")
        df['Оптовая цена'] = df['Оптовая цена'].fillna(0).astype('float')
        df['Розничная цена'] = df['Розничная цена'].str.replace(",", ".")
        df['Розничная цена'] = df['Розничная цена'].str.replace(" ", "")
        df['Розничная цена'] = df['Розничная цена'].fillna(0).astype('float')
        df[['МНН', 'Упаковка ЛП']].apply(
            lambda x: x.str.replace("\n", " ").str.strip()
        )
        return df

    async def save_data(self):
        for df, ind in self.parse_data():
            assert df.shape[1] == 11, f"Number of columns in file {self.file} \
                is incorrect, shoud be 11 but now is {df.shape[1]}, \
                table number is {ind+1}"
            df = self.process_columns(df, ind)
            logger.info(f"Saving table {ind+1} ...")
            data: pd.DataFrame = df[[
                'ИД упаковки',
                'Торговая марка',
                'МНН',
                'Производитель',
                'Упаковка ЛП',
                'Номер регистрации',
                'Валюта',
                'Предельная цена',
                'Оптовая цена',
                'Розничная цена'
                ]]
            await self.data_repo.add(data)
            logger.info(f"Saved {data.shape[0]} rows")

    async def parse(self):
        await self.download_file()
        self.parse_data()
        await self.save_data()
