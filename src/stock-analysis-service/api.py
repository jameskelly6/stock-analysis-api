from fastapi import FastAPI
import uvicorn
from sqlmodel import SQLModel
from db import engine
from routers import stocks, portfolio

app = FastAPI()
app.include_router(stocks.router)
app.include_router(portfolio.router)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def welcome():
    """Return welcome message"""
    return{'message': "Welcome to the Stock Analysis Service"}


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)