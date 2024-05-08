import logging
from datetime import datetime
from pathlib import Path
import logging

from parsers.ru.ru_crawler import RuCrawler
from parsers.ru.ru_parser import RuFileParser
from parsers.ru.repository import DocumentRepo, DataRepo
from utils import get_latest_files

logger = logging.getLogger(__name__)


class RuService:
    def __init__(self, session):
        self.crawler = RuCrawler(RuCrawler.MAIN_URL)
        self.parser = RuFileParser()
        self.repo = DocumentRepo(session)
        self.data_repo = DataRepo(session)
        self.tables = ()
        self.headers = ()
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
            # self.headers = list(map(lambda c: c.replace('\n', ''), self.tables.iloc[1, 1:].values.tolist()))
            self.headers = self.tables.iloc[1, :]
            self.tables = self.tables.iloc[2:, :]
            self.tables.columns = self.headers

    def process_columns(self, df):
        df = df.iloc[2:, :]
        df = df[[
            'МНН',
            'Торговое наименование лекарственного препарата',
            'Лекарственная форма, дозировка, упаковка (полная)',
            'Владелец РУ/производитель/упаковщик/Выпускающий контроль',
            'Код АТХ',
            'Коли-\nчество в потреб. упаков-\nке',
            'Предельная цена руб. без НДС'
        ]]
        self.tables = df

    async def save_data(self):
        # assert table.shape[1] == 11, f"Number of columns in file {self.file} is incorrect"
        logger.info(self.headers)
        self.process_columns(self.tables)
        await self.data_repo.add(self.tables)

    async def parse(self):
        # await self.download_file()
        self.parse_data()
        await self.save_data()
