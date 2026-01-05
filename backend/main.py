from typing import Union
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import yahoo_fin.stock_info as si
# dow_list = si.tickers_nasdaq(True)
import yfinance as yf
###
# cd backend
# fastapi dev main.py
###

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],  # Both variations
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/search")
def search_stocks(q: Optional[str]):
    if not q:
        return {"detail": "no query param"}
    data = yf.Search(q).quotes
    return [
        {
            "ticker": r["symbol"],
            "name": r["shortname"]
        }
        for r in data[:5]
    ]
    #return {"results": data}
    