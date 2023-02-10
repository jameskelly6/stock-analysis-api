from sqlmodel import SQLModel, Field
from datetime import datetime

class PortfolioTransaction(SQLModel):
    Asset: str
    Equity: str
    Holding: float
    Price: float
    Date: datetime
    Compensation: float

    class Config:
        schema_extra = {
            "example": {
                "Asset": "Security",
                "Equity": "NVDA",
                "Holding": 240,
                "Price": 125.97,
                "Date": datetime(2022, 10, 3),
                "Compensation": 30232.8
            }
        }

class Portfolio(PortfolioTransaction, table=True):
    id: int | None = Field(primary_key=True, default=None)

class PortfolioOutput(PortfolioTransaction):
    id: int


class EquityInformation(SQLModel):
    Equity: str = Field(default=None, foreign_key="portfolio.Equity")
    Open: float
    High: float
    Low: float
    Close: float    
    Volume: int


    class Config:
        schema_extra = {
            "example": {
                "Equity": "NVDA",
                "Open": 155.07,
                "High": 159.61,
                "Low": 154.72,
                "Close": 159.09,
                "Volume": 38410100
            }
        }

class Equity(EquityInformation, table=True):
    equity_id: int | None = Field()
