from parsers.kaz.kaz_crawler import KazCrawler
from parsers.kaz.kaz_parser import KazFileParser
from parsers.kaz.repository import DocumentRepo, DataRepo
from utils import get_latest_files

from pathlib import Path
import pandas as pd
import logging


logger = logging.getLogger(__name__)


class KazService:
    def __init__(self, session):
        self.crawler = KazCrawler(KazCrawler.MAIN_URL)
        self.parser = KazFileParser()
        self.repo = DocumentRepo(session)
        self.data_repo = DataRepo(session)
        self.tables = ()
        self.file = ''
        self.headings = ()
        self.cache = []
        self.number_of_tables = 0

    async def download_file(self):
        initial_page = self.crawler.get_page()
        if initial_page:
            iframe_page = self.crawler.find_iframe_link(initial_page)
            if iframe_page:
                document_page = self.crawler.find_document_link(iframe_page)
                if document_page:
                    self.file = self.crawler.load_document(document_page)

    def process_headings(self, headings: list):
        return list(map(lambda x: x.replace('\n', ''), headings))

    def parse_data(self):
        file = get_latest_files(KazCrawler.DOCUMENTS_DIRECTORY)
        if file:
            file_path = Path(
                KazCrawler.GENERAL_DOCUMENTS_DIRECTORY,
                KazCrawler.DOCUMENTS_DIRECTORY,
                file
            )
            self.file = file_path
            file = self.parser.read_file(file_path)
            for ind, page in enumerate(file):
                if ind == 0:
                    self.number_of_tables = page
                    logger.info(f"Found {self.number_of_tables} tables")
                    continue
                if len(page) == 0:
                    # if no tables on page
                    continue
                # if ind > 8:
                #     break
                # if headingd not set yet and there are tables on page
                if len(page[0]) != 0 and not self.headings:
                    self.headings = self.process_headings(page[0][0])
                    data = page[0][1:]
                else:
                    data = page[0]
                yield pd.DataFrame(data, columns=self.headings), ind

    def fix_broken_rows(self):
        if len(self.cache) != 0:
            fixed_row = ['' for _ in range(len(self.cache[0]))]
            for row in self.cache:
                for col_index, col in enumerate(row):
                    fixed_row[col_index] += col
        else:
            fixed_row = self.cache[0]
        self.cache = []
        return fixed_row

    async def save_data(self):
        for df, ind in self.parse_data():
            # # df = self.process_columns(df, ind)
            data: pd.DataFrame = df[[
                'Торговоенаименование',
                'МНН',
                'Лекарственнаяформа',
                'Производитель',
                'Регистрационноеудостоверение',
                'Предельная ценапроизводителя'
            ]]
            converted_data = data.values.tolist()
            if ind != 0:
                self.cache.append(converted_data[0])
                converted_data[0] = self.fix_broken_rows()
            if ind != self.number_of_tables - 1:
                self.cache.append(converted_data[-1])
                converted_data = converted_data[:-1]
            # logger.info(converted_data)
            await self.data_repo.add(converted_data)
            logger.info(f"Saved {data.shape[0]} rows")

    async def parse(self):
        # await self.download_file()
        await self.save_data()
