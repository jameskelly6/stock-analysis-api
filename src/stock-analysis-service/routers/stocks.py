import yfinance as yf
from historical_data import data_to_dict
from fastapi import Depends, HTTPException, APIRouter

router = APIRouter(prefix="/stock/{ticker}")

@router.get("/info")
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


@router.get("/data")
async def get_stock_data(ticker: str = None):
    ticker = yf.Ticker(ticker)
    data = ticker.history(period="1mo")
    json = data_to_dict(data)
    return json