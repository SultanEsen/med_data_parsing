from parsers.kz.kaz_crawler import KazCrawler
from parsers.kz.kaz_parser import KazFileParser
from parsers.kz.repository import DocumentRepo, DataRepo
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
                if len(page) == 0:
                    # if no tables on page
                    continue
                # if ind > 3:
                #     break
                # if headingd not set yet and there are tables on page
                if len(page[0]) != 0 and not self.headings:
                    self.headings = self.process_headings(page[0][0])
                    data = page[0][1:]
                else:
                    data = page[0]
                yield pd.DataFrame(data, columns=self.headings), ind

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
            await self.data_repo.add(data.values.tolist())
            logger.info(f"Saved {data.shape[0]} rows")

    async def parse(self):
        # await self.download_file()
        await self.save_data()
