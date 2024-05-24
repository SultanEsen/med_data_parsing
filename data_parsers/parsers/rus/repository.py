from datetime import datetime
import logging


class DocumentRepo:
    def __init__(self, session):
        self.session = session

    async def add(self, url):
        item = await self.session.execute(
            """
            INSERT INTO latest_documents (url, created_at) VALUES (?, ?)
            """,
            (url, datetime.utcnow())
        )

    async def get(self, url):
        item = await self.session.fetch(
            """
            SELECT * FROM latest_documents WHERE url = ?
            """,
            (url,),
            fetch_type="one"
        )
        return item

    async def list(self):
        items = await self.session.fetch(
            """
            SELECT * FROM latest_documents
            """,
            fetch_type="all"
        )
        return items


class DataRepo:
    def __init__(self, session):
        self.session = session

    async def add(self, df):
        for _, row in df.iterrows():
            await self.session.execute(
                """
                INSERT INTO russia_data
                (mnn, trade_mark_name,
                 medicine_info, producer, ath_code, amount, 
                 limit_price) VALUES
                (?, ?, ?, ?, ?, ?, ?)
                """,
                # The number of columns in the table is 11,
                # we are sving only 10 for now
                row
            )

    async def count(self):
        count = await self.session.fetch(
            """
            SELECT COUNT(*) FROM russia_data
            """
        )
        return count

    async def get(self, id):
        item = await self.session.fetch(
            """
            SELECT * FROM russia_data WHERE id = ?
            """,
            (id,),
            fetch_type="one"
        )
        return item

    async def list(self):
        items = await self.session.fetch(
            """
            SELECT * FROM russia_data
            """,
            fetch_type="all"
        )
        return items
