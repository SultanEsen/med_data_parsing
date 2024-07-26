from fastapi import FastAPI, Request, Depends, Body
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging
from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel
from typing import Annotated, Optional

from src.database import Database
from src.models.uzb import UzbData, IDataResponse as UZBDataResponse
from src.models.turk import IDataResponse as TurkDataResponse
from src.models.kaz import KazData, IDataResponse as KazDataResponse
from src.models.rus import RussiaData
from src.queries import Queries


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")
# db_path = Path(__file__).parent.parent.parent / "db.sqlite3"
# database = Database(db_path)
load_dotenv(Path(__file__).parent.parent.parent / ".env")
database = Database(getenv("DATABASE_URL"))
origins = ["http://localhost:5173", "http://localhost:4173", "http://medical.zzdev.ru"]
# REDIS_DATA_URL = "redis://localhost:6379"
logger = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class SearchParams(BaseModel):
    mnn: str
    trade_mark_name: Optional[str] = None       
    # producer: Optional[str] = None
    # producer_country: Optional[str] = None
    dosage_form: str


class SearchData(BaseModel):
    # package_id: Optional[str]
    mnn: str
    trade_mark_name: Optional[str]
    producer: Optional[str]
    package: Optional[str]
    currency: Optional[str]
    limit_price: Optional[float]
    country: str

class SearchResponse(BaseModel):
    data: list[SearchData]
    count: int
    pages: int


@app.post("/search", response_model=SearchResponse)
async def search(
    data: Annotated[
        SearchParams, 
        Body(
            ...,
            examples={
                "mnn": "моксифлоксацин",
                "trade_mark_name": "Моксикум",
                "dosage_form": "таблетки"
            }
        )
    ]
):

    if data.mnn and data.trade_mark_name:
        uzb_query = Queries.SELECT_UZBEKISTAN_MNN_TRADEMARK
        params = (data.mnn, data.trade_mark_name)
    if not data.trade_mark_name:
        uzb_query = Queries.SELECT_UZBEKISTAN_MNN
        params = (data.mnn,)
    
    result_uzb = await database.fetch(
        query=uzb_query,
        params=params,      
        number=1000
    )
    result_uzb = [dict(row) for row in result_uzb]
    result_uzb = list(map(lambda row: {**row, 'country': 'UZB'}, result_uzb))

    if data.mnn and data.trade_mark_name:
        rus_query = Queries.SELECT_RUSSIA_MNN_TRADEMARK
        params = (data.mnn, data.trade_mark_name, f"%{data.dosage_form}%")
    if not data.trade_mark_name:
        rus_query = Queries.SELECT_RUSSIA_MNN
        params = (data.mnn, f"%{data.dosage_form}%")

    result_russia = await database.fetch(                       
        query=rus_query,
        params=params,
        number=2000
    )
    result_russia = [dict(row) for row in result_russia]
    result_russia = list(map(lambda row: {**row, 'country': 'RUS', 'currency': 'RUB'}, result_russia))

    if data.mnn and data.trade_mark_name:
        kaz_query = Queries.SELECT_KAZAKHSTAN_MNN_TRADEMARK
        params = (f"%{data.mnn}%", data.trade_mark_name, f"%{data.dosage_form}%")
    if not data.trade_mark_name:
        kaz_query = Queries.SELECT_KAZAKHSTAN_MNN
        params = (f"%{data.mnn}%", f"%{data.dosage_form}%")

    result_kazakhstan = await database.fetch(
        query=kaz_query,
        params=params,
        number=1000
    )
    result_kazakhstan = [dict(row) for row in result_kazakhstan]
    result_kazakhstan = list(map(lambda row: {**row, 'country': 'KAZ', 'currency': 'KZT'}, result_kazakhstan))

    return_json =  result_kazakhstan+result_uzb+result_russia          

    return {
        "data": return_json,
        "count": len(return_json)
    }
    


@app.get("/uzb", response_model=UZBDataResponse)
async def uzbekistan_data(page: int = 1):
    """Эндпоинт для данных по Узбекистану"""
    data = await database.fetch(
        """SELECT * FROM uzbekistan_data LIMIT 20 OFFSET $1""",
        params=((page - 1) * 20,),
        number=20
    )
    meta_data = await database.count("uzbekistan_data")
    return {
        "data": [dict(row) for row in data],
        "pages": meta_data.get("count", 0) // 20 + 1,
        "page": page,
        "columns": list(UzbData.__fields__.keys()),
    }


@app.get("/turk", response_model=TurkDataResponse)
async def turkey_data(page: int = 1):
    """Эндпоинт для данных по Турции"""
    data = await database.fetch(
        """SELECT * FROM turkey_data LIMIT 20 OFFSET $1""",
        ((page - 1) * 20,),
        fetch_type="all",
    )
    meta_data = await database.fetch(
        """SELECT COUNT(*) FROM turkey_data""",
        fetch_type="one",
    )
    return {
        "data": data,
        "pages": meta_data["COUNT(*)"] // 20 + 1,
        "page": page,
        "columns": [
            "id",
            "medicine_info",
            "company_name",
            "price",
        ],
    }


@app.get("/kaz", response_model=KazDataResponse)
async def kazakhstan_data(page: int = 1):
    """Эндпоинт для данных по Казахстану"""
    data = await database.fetch(
        """SELECT * FROM kazakhstan_data LIMIT 20 OFFSET $1""",
        params=((page - 1) * 20,),
        number=20
    )
    meta_data = await database.count("kazakhstan_data")
    return {
        "data": [dict(row) for row in data],
        "pages": meta_data.get("count", 0) // 20 + 1,
        "page": page,
        "columns": list(KazData.__fields__.keys())
    }


@app.get("/rus")
async def russian_data(page: int = 1):
    """Эндпоинт для данных по России"""
    data = await database.fetch(
        """SELECT * FROM russia_data LIMIT 20 OFFSET $1""",
        params=((page - 1) * 20,),
        number=20
    )
    meta_data = await database.count("russia_data")
    return {
        "data": data,
        "pages": meta_data.get("count", 0) // 20 + 1,
        "page": page,
        "columns": list(RussiaData.__fields__.keys())
    }


@app.get("/rus/2")
async def russian_data2(request: Request, response: Response, page: int = 1):

    i = 1
    for dt in RussiaData.all_pks():
        logger.info(dt)
        i += 1
        if i > 10:
            break

    return {
        "data": "data",
        "pages": 1,
        "page": 1,
        "columns": [
            "id",
            "mnn",
            "trade_mark_name",
            "medicine_info",
            "producer",
            "ath_code",
            "amount",
            "limit_price",
        ],
    }


@app.get("/by", status_code=404)
async def belarus_data(page: int = 1):
    """Эндпоинт для данных по Беларуси"""
    return {}


@app.get("/ukr", status_code=404)
async def ukraine_data(page: int = 1):
    """Эндпоинт для данных по Украине"""
    return {}


@app.get("/mld", status_code=404)
async def moldova_data(page: int = 1):
    """Эндпоинт для данных по Молдове"""
    return {}

