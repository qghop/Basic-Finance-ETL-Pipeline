import yfinance as yf
import polars as pl
from datetime import datetime
import os

def fetch_stock_data(ticker_str, start, end):
    df = yf.download(ticker_str, start=start, end=end, auto_adjust=True, progress=False)
    if df is not None:
        df.reset_index(inplace=True)
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        pl_df = pl.from_pandas(df)
        print(pl_df.columns)
        return pl_df
    else:
        raise ValueError(f"No data found for ticker: {ticker_str}")

def save_raw_data(ticker_str, df):
    os.makedirs("data/bronze", exist_ok=True)
    df.write_ipc(f"data/bronze/{ticker_str}_raw.feather")

if __name__ == "__main__":
    ticker_str = "AAPL"
    start = "2020-01-01"
    end = datetime.today().strftime('%Y-%m-%d')
    df = fetch_stock_data(ticker_str, start, end)
    save_raw_data(ticker_str, df)
