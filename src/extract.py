import yfinance as yf
import polars as pl
from datetime import datetime
import os

def fetch_stock_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    if df is not None:
        df.reset_index(inplace=True)
        pl_df = pl.from_pandas(df)
        return pl_df
    else:
        raise ValueError(f"No data found for ticker: {ticker}")

def save_bronze_data(ticker: str, df: pl.DataFrame):
    os.makedirs("data/bronze", exist_ok=True)
    df.write_ipc(f"data/bronze/{ticker}.feather")

if __name__ == "__main__":
    ticker = "AAPL"
    start = "2020-01-01"
    end = datetime.today().strftime('%Y-%m-%d')
    df = fetch_stock_data(ticker, start, end)
    save_bronze_data(ticker, df)
