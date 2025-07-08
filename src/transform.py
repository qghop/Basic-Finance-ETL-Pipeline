import polars as pl
import os

def clean_raw_data(ticker_str):
    df = pl.read_ipc(f"data/bronze/{ticker_str}_raw.feather")

    df = df.with_columns([
        (pl.col("Close") - pl.col("Open")).alias("Price_Diff"),
        (pl.col("Close").pct_change() * 100).alias("Daily_Return"),
        pl.col("Close").rolling_mean(window_size=20).alias("SMA_20"),
        pl.col("Close").rolling_mean(window_size=50).alias("SMA_50")
    ]).drop_nulls()

    os.makedirs("data/silver", exist_ok=True)
    df.write_ipc(f"data/silver/{ticker_str}_cleaned.feather")

if __name__ == "__main__":
    clean_raw_data("AAPL")
