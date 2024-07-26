# from redis_om import HashModel
from pydantic import BaseModel


class RussiaData(BaseModel):
    id: int
    mnn: str
    trade_mark_name: str
    medicine_info: str
    producer: str
    ath_code: str
    amount: int | str
    limit_price: float