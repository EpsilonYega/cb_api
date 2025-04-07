from pydantic import BaseModel
from datetime import date

class CurrencyRateCreate(BaseModel):
    date: date
    currency_name: str
    vunit_rate: float

class CurrencyRateResponse(BaseModel):
    id: int
    date: date
    currency_name: str
    vunit_rate: float

    class Config:
        orm_mode = True