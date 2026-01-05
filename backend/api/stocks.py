from typing import Union
from typing import Optional

from fastapi import APIRouter
import yfinance as yf
from models.stock import StockRequest
from services.sentiment import analyze_sentiment

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@router.get("/search")
def search_stocks(q: Optional[str]):
    if not q:
        return {"detail": "no query param"}
    data = yf.Search(q).quotes
    return [
        {
            "ticker": r["symbol"],
            "name": r["shortname"]
        }
        for r in data[:5] # return the first 5 results
    ]

@router.post("/stock-sentiment")
def stock_sentiment(stock : StockRequest):
    return analyze_sentiment(stock)