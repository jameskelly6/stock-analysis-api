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