import pandas as pd
import yfinance as yf

def data_to_dict(data):
    dict = []
    df = pd.DataFrame(data=data)
    dict = df.to_dict('index')
    return dict
