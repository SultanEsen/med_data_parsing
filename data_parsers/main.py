import asyncio
import logging
from pprint import pprint
from pathlib import Path

from parsers.database import Database
from parsers.uzb.service import UZBService
from parsers.kz.service import KAZService
from parsers.tr.service import TURKService


logger = logging.getLogger(__name__)


async def main():
    # create database
    db_path = Path(__file__).parent.parent / "db.sqlite3"
    print(db_path)
    database = Database(db_path)
    await database.create_tables()

    # crawl and parse
    # service = UZBService(database)
    # await service.parse()
    # pprint(await service.data_repo.list())

    # service = KAZService()
    # await service.parse()

    service = TURKService(database)
    await service.parse()
    print("Count: ", await service.data_repo.count())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # run main function
    asyncio.run(main())
