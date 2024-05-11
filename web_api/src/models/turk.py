from pydantic import BaseModel


class TurkData(BaseModel):
    id: int
    medicine_info: str
    company_name: str
    price: float


class IDataResponse(BaseModel):
    data: list[TurkData]
    pages: int
    page: int
    columns: list[str]
