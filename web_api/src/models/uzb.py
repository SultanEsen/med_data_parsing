from pydantic import BaseModel


class UzbData(BaseModel):
    id: int
    package_id: int
    trade_mark_name: str
    mnn: str
    producer: str
    package: str
    registration_number: str
    currency: str
    limit_price: float
    current_retail_price: str
    current_wholesale_price: str


class IDataResponse(BaseModel):
    data: list[UzbData]
    pages: int
    page: int
    columns: list[str]
