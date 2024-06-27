import logging

logger = logging.getLogger(__name__)


class DataRepo:
    def __init__(self, session):
        self.session = session

    async def add(self, df):
        for i, row in df.iterrows():
            # record = await self.session.fetch(
            #     "SELECT * FROM russia_data WHERE mnn = $1 AND medicine_info = $2 and amount = $3",
            #     params=(row.iloc[0], row.iloc[2], row.iloc[5]),
            # )
            logger.info(f"Row: {i}")
            await self.session.execute(
                """
                INSERT INTO russia_data
                (mnn, trade_mark_name,
                 medicine_info, producer, ath_code, amount,
                 limit_price) VALUES
                ($1, $2, $3, $4, $5, $6, $7)
                """,
                tuple(row.values),
            )

    async def copy_from_csv(self, path):
        logger.info(f"Path: {path}")
        await self.session.execute(
            f"""
            COPY russia_data(
                mnn, trade_mark_name,
                medicine_info, producer, ath_code, amount,
                limit_price
            ) FROM {path}
            WITH DELIMITER AS ','
            CSV HEADER
            """
        )

    async def count(self):
        count = await self.session.fetch(
            """
            SELECT COUNT(*) FROM russia_data
            """
        )
        return count

    async def get(self, record_id):
        item = await self.session.fetch(
            """
            SELECT * FROM russia_data WHERE id = ?
            """,
            (record_id,),
            fetch_type="one",
        )
        return item

    async def list(self):
        items = await self.session.fetch(
            """
            SELECT * FROM russia_data
            """,
            fetch_type="all",
        )
        return items


# class DocumentRepo:
#     def __init__(self, session):
#         self.session = session

#     async def add(self, url):
#         item = await self.session.execute(
#             """
#             INSERT INTO latest_documents (url, created_at) VALUES (?, ?)
#             """,
#             (url, datetime.utcnow())
#         )

#     async def get(self, url):
#         item = await self.session.fetch(
#             """
#             SELECT * FROM latest_documents WHERE url = ?
#             """,
#             (url,),
#             fetch_type="one"
#         )
#         return item

#     async def list(self):
#         items = await self.session.fetch(
#             """
#             SELECT * FROM latest_documents
#             """,
#             fetch_type="all"
#         )
#         return items
