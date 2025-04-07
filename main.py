from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from database import SessionLocal
from schemas import CurrencyRateCreate, CurrencyRateResponse
from crud import create_currency_rate, get_currency_rates

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=list[CurrencyRateResponse])
async def root(db: Session = Depends(get_db)):
    r = httpx.get('http://www.cbr.ru/scripts/XML_daily.asp')
    if r.status_code == 200:
        xml_content = r.text
        try:
            root = ET.fromstring(xml_content)
            for child in root:
                name = child.find("Name").text.strip() if child.find("Name") is not None else None
                vunit_rate_text = child.find("VunitRate").text.strip().replace(',', '.') if child.find("VunitRate") is not None else None
                vunit_rate = float(vunit_rate_text) if vunit_rate_text else None

                rate = CurrencyRateCreate(
                    date=datetime.now().date(),
                    currency_name=name,
                    vunit_rate=vunit_rate
                )
                create_currency_rate(db, rate)
        except ET.ParseError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка парсинга XML: {e}")
    else:
        raise HTTPException(status_code=r.status_code, detail="Ошибка HTTP при запросе к ЦБ РФ")

    return get_currency_rates(db)
