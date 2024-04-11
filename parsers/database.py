import aiosqlite

from parsers.queries import Queries


class Database:
    def __init__(self, path):
        self.path = path

    async def create_tables(self):
        async with aiosqlite.connect(self.path) as conn:
            await conn.execute(Queries.CREATE_LATEST_DOCUMENTS_TABLE)
            await conn.execute(Queries.CREATE_UZBEKISTAN_DATA_TABLE)
            await conn.commit()

    async def fetch(self, query: str, params: tuple = (), fetch_type: str = "all"):
        async with aiosqlite.connect(self.path) as conn:
            cursor = await conn.execute(query, params)
            if fetch_type == "one":
                return await cursor.fetchone()
            elif fetch_type == "all":
                return await cursor.fetchall()

    async def execute(self, query: str, params: tuple = ()):
        async with aiosqlite.connect(self.path) as conn:
            await conn.execute(query, params)
            await conn.commit()
