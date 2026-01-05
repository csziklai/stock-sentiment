from pydantic import BaseModel

class StockRequest(BaseModel):
    ticker: str
    name: str