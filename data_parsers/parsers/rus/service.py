import logging
from datetime import datetime
from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile

import httpx
from utils import get_latest_files, wait_for_download
from config import PROJECT_ROOT

from parsers.repository import DocumentRepo
from parsers.rus.repository import DataRepo
from parsers.rus.ru_crawler import RuCrawler
from parsers.rus.ru_parser import RuFileParser

logger = logging.getLogger(__name__)


class RuService:
    def __init__(self, session):
        self.downloader = httpx.AsyncClient()
        self.crawler = RuCrawler(
            url=RuCrawler.MAIN_URL, 
            download_dir=Path(
                PROJECT_ROOT, 
                RuCrawler.GENERAL_DOCUMENTS_DIRECTORY,
                RuCrawler.DOCUMENTS_DIRECTORY
            )
        )
        self.parser = RuFileParser()
        self.repo = DocumentRepo(session)
        self.data_repo = DataRepo(session)
        self.tables = ()
        self.headers = ()
        self.zipfile = None
        self.file = None

    async def download_file(self):
        try:
            self.crawler.start()
            self.crawler.get_page()
            self.crawler.find_date_link()
            file_url = self.crawler.find_latest_document()
            logger.info(f"Found {file_url} for RUSSIA")
            item = await self.repo.get(file_url)
            if not item:
                logger.info(f"Downloading {file_url} for RUSSIA")
                # file = await self.downloader.get(file_url)
                file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                download_dir = Path(self.crawler.download_dir, "tmp/")
                download_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Download dir: {download_dir}")
                downloaded_file = Path(self.crawler.download_dir, f"tmp/{file_name}.zip")
                with open(downloaded_file, "wb") as f:
                    async with self.downloader.stream(method="GET", url=file_url, timeout=120) as file:
                        async for chunk in file.aiter_bytes():
                            f.write(chunk)
                if not await wait_for_download(file_location=download_dir, file_name=f"{file_name}.zip", timeout=120):
                    raise TimeoutError("Download timeout")
                await self.repo.add(url=file_url, country="rus")
                logger.info(f"Downloaded {downloaded_file}")

                return downloaded_file
            # if self.crawler.wait_for_download():
            #     return self.crawler.download_dir
            # else:
            #     raise TimeoutError("Download timeout")
        finally:
            self.crawler.driver.close()
            await self.downloader.aclose()
        # initial_page = self.crawler.get_page()
        # logging.info("Searching ...")
        # link = self.crawler.find_date_link(initial_page)
        # return
        # urls = self.crawler.find_latest_document(initial_page)
        # logging.info(f"Found {urls}")
        # if urls:
        #     item = await self.repo.get(urls)
        #     if not item:
        #         logging.info("Downloading file ...")
        #         self.zipfile = self.crawler.load_document(urls)

    def extract_archive(self, downloaded_file: Path):
        # await self.repo.add(urls)
        logger.info("Extracting archive ...  %s", downloaded_file)
        if downloaded_file is not None:
            self.zipfile = downloaded_file
            file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            with ZipFile(self.zipfile, "r") as zipref:
                zipref.extractall(path=self.crawler.download_dir)
            self.file = Path(self.crawler.download_dir, f"{file_name}.xlsx")

            rmtree(Path(self.crawler.download_dir, "tmp/"))

    def parse_data(self):
        file = get_latest_files(RuCrawler.DOCUMENTS_DIRECTORY)

        if file:
            file_path = Path(
                RuCrawler.GENERAL_DOCUMENTS_DIRECTORY,
                RuCrawler.DOCUMENTS_DIRECTORY,
                file,
            )
            self.file = file_path
            self.tables = self.parser.read_file(self.file)
            # self.headers = list(map(lambda c: c.replace(
            #     '\n',
            #     ''
            # ), self.tables.iloc[1, 1:].values.tolist()))
            self.headers = self.tables.iloc[1, :]
            self.tables = self.tables.iloc[2:, :]
            self.tables.columns = self.headers

    def process_columns(self, df):
        """
        Здесь описывается, какие колонки будут браться из выборки
        а также как некоторые колонки преобразовываются
        """

        # df = df.iloc[2:1000, :]
        self.headers = [
            "МНН",
            "Торговое наименование лекарственного препарата",
            "Лекарственная форма, дозировка, упаковка (полная)",
            "Владелец РУ/производитель/упаковщик/Выпускающий контроль",
            "Код АТХ",
            "Коли-\nчество в потреб. упаков-\nке",
            "Предельная цена руб. без НДС",
        ]
        df = df[self.headers]
        df["Код АТХ"] = df["Код АТХ"].astype(str)
        df["МНН"] = df["МНН"].astype(str)
        df["Коли-\nчество в потреб. упаков-\nке"] = df["Коли-\nчество в потреб. упаков-\nке"].fillna(0).astype(int)
        self.tables = df
        self.headers = [
            "МНН",
            "Торговое наименование лекарственного препарата",
            "Лекарственная форма, дозировка, упаковка (полная)",
            "Владелец РУ/производитель/упаковщик/Выпускающий контроль",
            "Код АТХ",
            "Количество в потреб. упаковке",
            "Предельная цена руб. без НДС"
        ]
        df.columns = self.headers

    def divide_into_chunks(self, df, n):
        # looping till length of data
        for i in range(0, len(df), n):
            # start = perf_counter()
            yield df.iloc[i : i + n]
            # end = perf_counter()
            # logger.info(f"{(end - start) * 1000} ms")

    def copy_csv(self):
        # self.tables.drop(self.tables.index[0], axis=0, inplace=True)
        self.tables.to_csv(Path(self.crawler.download_dir, "rus.csv"), index=False)
        # await self.data_repo.copy_from_csv(f"{Path(PROJECT_ROOT, self.crawler.download_dir)}/rus.csv")
        # logger.info(f"Data successfully saved from file {self.file}")


    async def save_data(self):
        self.process_columns(self.tables)
        # if len(self.tables) > 5_000:
        #     for ind, chunk in enumerate(self.divide_into_chunks(
        #         self.tables,
        #         100
        #     )):
        #         logger.info(f"Saving chunk {ind}")
        #         await self.data_repo.add(chunk)
        # else:
        #     await self.data_repo.add(self.tables)
        # await self.data_repo.add(self.tables)
        self.copy_csv()


    async def parse(self):
        """
        Общий метод, в котором описан сам процесс загрузки,
        предварительной обработки и сохранения скачанной информации
        """

        # file = await self.download_file()
        # if file is not None:
        #     self.extract_archive(file)
        self.parse_data()
        await self.save_data()
        logger.info(f"Count: {await self.data_repo.count()}")
