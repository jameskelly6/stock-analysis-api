from scehmas import Portfolio, PortfolioTransaction
import yfinance as yf

def pc_roi(portfolio_input: Portfolio):
    ticker = yf.Ticker(portfolio_input.Equity)
    price = ticker.info['regularMarketPrice']
    pc_raw = (price - portfolio_input.Price)/(portfolio_input.Price)
    pc_total = round(pc_raw*100, 2)
    total_roi = round(pc_raw*portfolio_input.Compensation, 2)
    return pc_total, total_roi


