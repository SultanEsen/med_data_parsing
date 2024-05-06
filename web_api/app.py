from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from pprint import pprint

from database import Database
from models.uzb import IDataResponse as UZBDataResponse
from models.turk import IDataResponse as TurkDataResponse
from models.kaz import IDataResponse as KazDataResponse


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")
db_path = Path(__file__).parent.parent / "db.sqlite3"
database = Database(db_path)
origins = ["http://localhost:5173", "http://localhost:4173", "https://medd.zzdev.ru"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/uzb", response_model=UZBDataResponse)
async def uzbekistan_data(page: int = 1):
    """Эндпоинт для данных по Узбекистану"""
    data = await database.fetch(
        """SELECT * FROM uzbekistan_data LIMIT 20 OFFSET ?""",
        ((page - 1) * 20,),
        fetch_type="all",
    )
    meta_data = await database.fetch(
        """SELECT COUNT(*) FROM uzbekistan_data""",
        fetch_type="one",
    )
    return {
        "data": data,
        "pages": meta_data['COUNT(*)'] // 20 + 1,
        "page": page,
        "columns": [
            "id",
            "package_id",
            "trade_mark_name",
            "mnn",
            "producer",
            "package",
            "registration_number",
            "currency",
            "limit_price",
            "current_retail_price",
            "current_wholesale_price",
        ],
    }

@app.get("/turk", response_model=TurkDataResponse)
async def turkey_data(page: int = 1):
    """Эндпоинт для данных по Турции"""
    data = await database.fetch(
        """SELECT * FROM turkey_data LIMIT 20 OFFSET ?""",
        ((page - 1) * 20,),
        fetch_type="all",
    )
    meta_data = await database.fetch(
        """SELECT COUNT(*) FROM turkey_data""",
        fetch_type="one",
    )
    return {
        "data": data,
        "pages": meta_data['COUNT(*)'] // 20 + 1,
        "page": page,
        "columns": [
            "id",
            "medicine_info",
            "company_name",
            "price",
        ]
    }


@app.get("/kaz", response_model=KazDataResponse)
async def kazakhstan_data(page: int = 1):
    """Эндпоинт для данных по Казахстану"""
    data = await database.fetch(
        """SELECT * FROM kazakhstan_data LIMIT 20 OFFSET ?""",
        ((page - 1) * 20,),
        fetch_type="all",
    )
    meta_data = await database.fetch(
        """SELECT COUNT(*) FROM kazakhstan_data""",
        fetch_type="one",
    )
    return {
        "data": data,
        "pages": meta_data['COUNT(*)'] // 20 + 1,
        "page": page,
        "columns": [
            "id",
            "trade_mark_name",
            "mnn",
            "dosage_form",
            "producer",
            "registration_number",
            "limit_price"
        ]
    }


@app.get("/rus")
async def russian_data(page: int = 1):
    """Эндпоинт для данных по России"""
    data = await database.fetch(
        """SELECT * FROM russia_data LIMIT 20 OFFSET ?""",
        ((page - 1) * 20,),
        fetch_type="all",
    )
    meta_data = await database.fetch(
        """SELECT COUNT(*) FROM russia_data""",
        fetch_type="one",
    )
    return {
        "data": data,
        "pages": meta_data['COUNT(*)'] // 20 + 1,
        "page": page,
        "columns": [
            "id",
            "mnn",
            "trade_mark_name",
            "medicine_info",
            "producer",
            "ath_code",
            "amount",
            "limit_price"
        ]
    }


@app.get("/blr", status_code=404)
async def belarus_data(page: int = 1):
    """Эндпоинт для данных по Беларуси"""
    return {}


@app.get("ukr", status_code=404)
async def ukraine_data(page: int = 1):
    """Эндпоинт для данных по Украине"""
    return {}


@app.get("/mld", status_code=404)
async def moldova_data(page: int = 1):
    """Эндпоинт для данных по Молдове"""
    return {}
