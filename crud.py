from sqlalchemy.orm import Session
from models import CurrencyRate
from schemas import CurrencyRateCreate

def create_currency_rate(db: Session, rate: CurrencyRateCreate):
    db_rate = CurrencyRate(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

def get_currency_rates(db: Session) -> List:
    return db.query(CurrencyRate).all()