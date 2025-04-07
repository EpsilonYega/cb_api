from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    currency_name = Column(String, nullable=False)
    vunit_rate = Column(Float, nullable=False)