import polars as pl
import os

def calculate_rsi(df, window = 14):
    gains = df.select(pl.when(pl.col("Daily_Return") > 0).then(pl.col("Daily_Return")).otherwise(0.0).alias("gain"))["gain"]
    losses = df.select(pl.when(pl.col("Daily_Return") < 0).then(-pl.col("Daily_Return")).otherwise(0.0).alias("loss"))["loss"]

    avg_gain = gains.rolling_mean(window_size=window, min_periods=1)
    avg_loss = losses.rolling_mean(window_size=window, min_periods=1)

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def generate_rsi_signal(ticker_str):
    df = pl.read_ipc(f"data/silver/{ticker_str}_cleaned.feather")

    rsi = calculate_rsi(df)
    df = df.with_columns(rsi.alias(f"RSI"))

    df = df.with_columns([
        (pl.col(f"RSI") < 30).alias("Oversold_Signal"),
        (pl.col(f"RSI") > 70).alias("Overbought_Signal")
    ])

    os.makedirs("data/gold", exist_ok=True)
    df.write_ipc(f"data/gold/{ticker_str}_signals.feather")

if __name__ == "__main__":
    generate_rsi_signal("AAPL")
