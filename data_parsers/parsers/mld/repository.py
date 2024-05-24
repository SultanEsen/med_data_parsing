
class DataRepo:
    def __init__(self, session):
        self.session = session

    async def add(self, df):
        for _, row in df.iterrows():
            # logging.info(row.iloc[0:10])
            await self.session.execute(
                """
                INSERT INTO moldova_data
                (trade_mark_name,
                medical_form,
                dosage_form,
                volume,
                producer_country,
                producer,
                ath_code,
                mnn,
                price,
                currency) VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                # The number of columns in the table is 11,
                # we are sving only 10 for now
                row
            )

    async def count(self):
        count = await self.session.fetch(
            """
            SELECT COUNT(*) FROM moldova_data
            """
        )
        return count

    async def get(self, id):
        item = await self.session.fetch(
            """
            SELECT * FROM moldova_data WHERE id = ?
            """,
            (id,),
            fetch_type="one"
        )
        return item

    async def list(self):
        items = await self.session.fetch(
            """
            SELECT * FROM moldova_data
            """,
            fetch_type="all"
        )
        return items


"""
    trade_mark_name,
    medical_form,
    dosage_form,
    volume,
    producer_country,
    producer,
    ath_code,
    mnn,
    price,
    currency
"""
