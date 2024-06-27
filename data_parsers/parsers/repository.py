from datetime import datetime
from enum import Enum


class Country(Enum):
    KAZ = "kaz"
    RUS = "rus"
    TURK = "turk"
    UZB = "uzb"
    MLD = "mld"
    BY = "by"


class DocumentRepo:
    def __init__(self, session):
        self.session = session

    async def add(self, country: Country, url: str):
        """
        Parameters:
            country: one of the countries: kaz, rus, turk, uzb, mld, by
            url: url of the document
        """
        item = await self.session.execute(
            """
            INSERT INTO latest_documents
            (url, country, created_at) VALUES ($1, $2, $3)
            """,
            (url, country, datetime.utcnow()),
        )
        return item

    async def get(self, url):
        item = await self.session.fetch(
            """
            SELECT * FROM latest_documents WHERE url = $1
            """,
            params=(url,),
        )
        return item

    async def list(self, number):
        items = await self.session.fetch(
            """
            SELECT * FROM latest_documents
            """,
            number=number,
        )
        return items
