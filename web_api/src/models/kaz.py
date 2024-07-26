from pydantic import BaseModel


class KazData(BaseModel):
    id: int
    trade_mark_name: str
    mnn: str
    dosage_form: str
    producer: str
    registration_number: str
    limit_price: str|float


class IDataResponse(BaseModel):
    data: list[KazData]
    pages: int
    page: int
    columns: list[str]
