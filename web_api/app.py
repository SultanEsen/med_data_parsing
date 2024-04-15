from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from pprint import pprint

from database import Database
from models.uzb import IDataResponse, UzbData


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


@app.get("/uzb", response_model=IDataResponse)
async def root(page: int = 1):
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
