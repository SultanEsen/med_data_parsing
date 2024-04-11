import asyncio
import logging
from pprint import pprint
from pathlib import Path

from parsers.database import Database
from parsers.service import UZBService


async def main():
    # create database
    db_path = Path(__file__).parent / "db.sqlite3"
    print(db_path)
    database = Database(db_path)
    await database.create_tables()

    # crawl and parse
    service = UZBService(database)
    await service.parse()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # run main function
    asyncio.run(main())
