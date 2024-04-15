import aiosqlite


class Database:
    def __init__(self, path):
        self.path = path

    async def fetch(self, query: str, params: tuple = (), fetch_type: str = "all"):
        async with aiosqlite.connect(self.path) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(query, params)

            if fetch_type == "one":
                data = await cursor.fetchone()
                return dict(data)
            elif fetch_type == "all":
                data = await cursor.fetchall()
                return [dict(row) for row in data]

    async def execute(self, query: str, params: tuple = ()):
        async with aiosqlite.connect(self.path) as conn:
            await conn.execute(query, params)
            await conn.commit()
