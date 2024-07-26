# import aiosqlite
import asyncpg


class Database:
    def __init__(self, path):
        self.path = path

    async def fetch(self, query: str, number: int = 1, params: tuple = ()):
        conn = await asyncpg.connect(self.path)
        async with conn.transaction():
            # logger.info(f"Query: {query}, params: {params}")
            cusor = await conn.cursor(query, *params)
            result = await cusor.fetch(number)
            return result
        # async with aiosqlite.connect(self.path) as conn:
        #     conn.row_factory = aiosqlite.Row
        #     cursor = await conn.execute(query, params)

        #     if fetch_type == "one":
        #         data = await cursor.fetchone()
        #         return dict(data)
        #     elif fetch_type == "all":
        #         data = await cursor.fetchall()
        #         return [dict(row) for row in data]

    async def execute(self, query: str, params: tuple = ()):
        conn = await asyncpg.connect(self.path)
        await conn.execute(query, *params)
        # async with aiosqlite.connect(self.path) as conn:
        #     await conn.execute(query, params)
        #     await conn.commit()

    async def count(self, table_name: str, params: tuple = ("1=1")):
        conn = await asyncpg.connect(self.path)
        row_count = await conn.fetchrow(f"SELECT COUNT(*) FROM {table_name}")
        return row_count