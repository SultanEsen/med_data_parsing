from datetime import datetime
import logging


logger = logging.getLogger(__name__)


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
        return item

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

    # async def add(self, df):
    #     """ 
    #     old version
    #     """
    #     await self.session.execute_many(
    #         """
    #         INSERT INTO uzbekistan_data
    #         (package_id, trade_mark_name, mnn,
    #          producer, package, registration_number,
    #          currency, limit_price, current_retail_price,
    #          current_wholesale_price) VALUES
    #         (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    #         """,
    #         # The number of columns in the table is 11,
    #         # we are sving only 10 for now
    #         # (row.iloc[0:10])
    #         df
    #     )

    async def add(self, df):
        for i, row in df.iterrows():
            await self.session.execute(
                """ 
                INSERT INTO uzbekistan_data
                (package_id, trade_mark_name, mnn,
                producer, package, registration_number,
                currency, limit_price, current_retail_price,
                current_wholesale_price) VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """,
                row.iloc[0:10]
            )

    async def count(self):
        count = await self.session.fetch(
            """
            SELECT COUNT(*) FROM uzbekistan_data
            """
        )
        return count

    async def get(self, id):
        item = await self.session.fetch(
            """
            SELECT * FROM uzbekistan_data WHERE id = ?
            """,
            (id,),
            fetch_type="one"
        )
        return item

    async def list(self):
        items = await self.session.fetch(
            """
            SELECT * FROM uzbekistan_data
            """,
            fetch_type="all"
        )
        return items
