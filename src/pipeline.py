import extract
import transform
import signals
from datetime import datetime

def run_pipeline(ticker_str, start_date, end_date):
    extract.fetch_stock_data(ticker_str, start_date, end_date)
    transform.clean_raw_data(ticker_str)
    signals.generate_rsi_signal(ticker_str)
    
if __name__ == "__main__":
    ticker_str = "AAPL"
    start = "2020-01-01"
    end = datetime.today().strftime('%Y-%m-%d')
    run_pipeline(ticker_str, start, end)