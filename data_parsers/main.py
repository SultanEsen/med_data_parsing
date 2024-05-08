import asyncio
import logging
from pprint import pprint
from pathlib import Path

from parsers.database import Database
from parsers.uzb.service import UZBService
from parsers.kz.service import KazService
from parsers.tr.service import TURKService
from parsers.ru.service import RuService


logger = logging.getLogger(__name__)


async def main():
    # create database
    db_path = Path(__file__).parent.parent / "db.sqlite3"
    # print(db_path)
    database = Database(db_path)
    await database.create_tables()

    # crawl and parse
    service = UZBService(database)
    logger.info("Starting UZB")
    await service.parse()
    # pprint(await service.data_repo.list())

    service = KazService(database)
    logger.info("Starting KAZ")
    await service.parse()

    service = TURKService(database)
    logger.info("Starting TURK")
    await service.parse()
    # print("Count: ", await service.data_repo.count())

    service = RuService(database)
    logger.info("Starting RU")
    await service.parse()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # run main function
    asyncio.run(main())
