from fastapi import FastAPI
from api.stocks import router as stock_router
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(stock_router)
    