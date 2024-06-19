import asyncpg
import logging

from parsers.queries import Queries


logger = logging.getLogger(__name__)


class Database:
    def __init__(self, path):
        self.path = path

    async def create_tables(self):
        # conn = await asyncpg.connect('postgresql://postgres@localhost/test')
        conn = await asyncpg.connect(self.path)
        # await conn.execute(Queries.VACUUM)
        await conn.execute(Queries.CREATE_LATEST_DOCUMENTS_TABLE)
        # await conn.execute(Queries.DROP_UZBEKISTAN_DATA_TABLE)
        await conn.execute(Queries.CREATE_UZBEKISTAN_DATA_TABLE)
        # await conn.execute(Queries.DROP_TURKEY_DATA_TABLE)
        await conn.execute(Queries.CREATE_TURKEY_DATA_TABLE)
        # await conn.execute(Queries.DROP_KAZAKHSTAN_DATA_TABLE)
        await conn.execute(Queries.CREATE_KAZAKHSTAN_DATA_TABLE)
        await conn.execute(Queries.DROP_RUSSIA_DATA_TABLE)
        await conn.execute(Queries.CREATE_RUSSIA_DATA_TABLE)
        # await conn.commit()
        logger.info("Created tables")
        await conn.close()

    async def fetch(
        self,
        query: str,
        number: int = 1,
        params: tuple = (),
    ):
        conn = await asyncpg.connect(self.path)
        async with conn.transaction():
            # logger.info(f"Query: {query}, params: {params}")
            cusor = await conn.cursor(query, *params)
            result = await cusor.fetch(number)
            return result

    # async def fetch(
    #     self,
    #     query: str,
    #     params: tuple = (),
    #     fetch_type: str = "all"
    # ):
    #     async with aiosqlite.connect(self.path) as conn:
    #         cursor = await conn.execute(query, params)
    #         if fetch_type == "one":
    #             return await cursor.fetchone()
    #         elif fetch_type == "all":
    #             return await cursor.fetchall()

    async def execute(self, query: str, params: tuple = ()):
        # async with asyncpg.connect(self.path) as conn:
        conn = await asyncpg.connect(self.path)
        await conn.execute(query, *params)
        # await conn.commit()

    async def execute_many(
        self,
        query: str,
        params: tuple = ()
    ):
        """
        example:
            database.execute_many(
                '''
                INSERT INTO russia_data (mnn, trade_mark_name,
                medicine_info, producer, ath_code, amount,
                limit_price) VALUES
                (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    *row
                )
            )
        """
        conn = await asyncpg.connect(self.path)
        async with conn.transaction():
            await conn.execute(
                query,
                params
            )

    # async def execute_many(self, query: str, params: tuple = ()):
    #     async with asyncpg.connect(self.path) as conn:
    #         await conn.executemany(query, params)
            # await conn.commit()
