from datetime import datetime
import logging
from utils import isfloat, check_and_remove_space


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
    #     """old version of add"""
    #     await self.session.execute_many(
    #         """
    #             INSERT INTO kazakhstan_data (
    #                 trade_mark_name,
    #                 mnn,
    #                 dosage_form,
    #                 producer,
    #                 registration_number,
    #                 limit_price
    #             ) VALUES (?, ?, ?, ?, ?, ?)
    #         """,
    #         df
    #     )

    async def add(self, lst):
        for i, row in enumerate(lst):
            if isfloat(row[5]):
                row[5] = float(row[5].replace(',', '.'))
            else:
                row[5] = None
            # if row[1] and len(row[1])>9 and row[1][8] == ' ':
            #     row[1] = row[1][:8] + row[1][9:]
            row[1] = check_and_remove_space(row[1], 8)
            row[1] = check_and_remove_space(row[1], 9)
            logger.info(f"Row: {i}, {row}")
            await self.session.execute(
                """
                    INSERT INTO kazakhstan_data (
                        trade_mark_name,
                        mnn,
                        dosage_form,
                        producer,
                        registration_number,
                        limit_price
                    ) VALUES ($1, $2, $3, $4, $5, $6)
                """,
                row
            )

    async def count(self):
        count = await self.session.fetch(
            """
            SELECT COUNT(*) FROM kazakhstan_data
            """
        )
        return count

    async def get(self, id):
        item = await self.session.fetch(
            """
            SELECT * FROM kazakhstan_data WHERE id = ?
            """,
            (id,),
            fetch_type="one"
        )
        return item

    async def list(self):
        items = await self.session.fetch(
            """
            SELECT * FROM kazakhstan_data
            """,
            fetch_type="all"
        )
        return items
