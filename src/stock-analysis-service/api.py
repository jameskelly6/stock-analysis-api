from fastapi import FastAPI, HTTPException, Depends
from portfolio_calculations import pc_roi
import uvicorn
from sqlmodel import SQLModel, Session, select
import mysql.connector
from db import engine, get_session
from routers import stocks, portfolio

app = FastAPI()
app.include_router(stocks, portfolio)

mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword"
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def welcome():
    """Return welcome message"""
    return{'message': "Welcome to the Stock Analysis Service"}


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)