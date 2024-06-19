from redis_om import HashModel


class RussiaData(HashModel):
    mnn: str
    trade_mark_name: str
    medicine_info: str
    producer: str
    ath_code: str
    amount: int | str
    limit_price: float
