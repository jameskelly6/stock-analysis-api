from fastapi import FastAPI, HTTPException, Depends
from historical_data import data_to_dict
import yfinance as yf
from datetime import datetime
from portfolio_calculations import pc_roi
import uvicorn
from sqlmodel import SQLModel, create_engine, Session, select

from scehmas import PortfolioTransaction, PortfolioOutput, Portfolio

app = FastAPI()

engine = create_engine(
    "sqlite:///portfolio.db",
    connect_args={"check_same_thread": False}, # Needed for SQLite
    echo=True # Log generated SQL
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def welcome():
    """Return welcome message"""
    return{'message': "Welcome to the Stock Analysis Service"}


@app.get("/stock/{ticker}/info")
async def get_stock_info(ticker: str = None, metric: str = None):
    ticker = yf.Ticker(ticker)
    if metric:
        information = {metric: ticker.info[metric]}
    else:    
        information = []
        for info in ticker.info:
            information.append({
                info: ticker.info[info]
            })
    return information


@app.get("/stock/{ticker}/data")
async def get_stock_data(ticker: str = None):
    ticker = yf.Ticker(ticker)
    data = ticker.history(period="1mo")
    json = data_to_dict(data)
    return json


@app.get("/portfolio")
async def get_holding(ticker: str | None = None, security: str | None = None, session: Session=Depends(get_session)) -> list:
    query = select(Portfolio)
    roi_pc = 0
    roi_gain = 0
    if ticker:
        query=query.where(Portfolio.Equity == ticker)
    if security:
        query=query.where(Portfolio.Asset == security)
    items = session.exec(query).all()
    for stock in items:
        if ".L" in stock.Equity:
            symbol="£"
        else:
            symbol = "$"
        roi_pc = roi_pc + pc_roi(stock)[0]
        roi_gain = roi_gain + pc_roi(stock)[1]
    items.append({"Total return %": f"{roi_pc}%", "Total return": f"{symbol}{roi_gain}"})
    return items
        

@app.get("/portfolio/{id}", response_model=Portfolio)
def holding_by_id(id: int, session: Session=Depends(get_session)) -> Portfolio:
    holding = session.get(Portfolio, id)
    if holding:
        return holding
    else:
        raise HTTPException(status_code=404, detail=f"No holding with id={id}")


@app.post("/portfolio", response_model=Portfolio)
async def add_holding(portfolio_input: PortfolioTransaction, session: Session=Depends(get_session)) -> Portfolio:
    portfolio_input = Portfolio.from_orm(portfolio_input)
    session.add(portfolio_input)
    session.commit()
    session.refresh(portfolio_input)
    return portfolio_input
    

@app.delete("/portfolio/{id}")
async def portfolio(id: int = None, session: Session=Depends(get_session)) -> None:
    holding = session.get(Portfolio, id)
    if holding:
        session.delete(holding)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No holding with id={id}")

@app.put("/portfolio/{id}", response_model=Portfolio)
async def change_holding(id: int, new_data: PortfolioTransaction, session: Session=Depends(get_session)) -> Portfolio:
    holding = session.get(Portfolio, id)
    if holding:
        holding.Asset = new_data.Asset
        holding.Equity = new_data.Equity
        holding.Holding = new_data.Holding
        holding.Price = new_data.Price
        holding.Date = new_data.Date
        holding.Compensation = new_data.Compensation
        session.commit()
        return holding
    else:
        raise HTTPException(status_code=404, detail=f"No holding with id={id}")


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)