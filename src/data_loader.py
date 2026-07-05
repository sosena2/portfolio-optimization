import yfinance as yf
import pandas as pd
import os

def fetch_asset_data(tickers, start_date, end_date, save_dir="../data/processed"):
    """
    Fetch historical OHLCV data for a list of tickers from YFinance.
    Saves each ticker's data as a separate CSV and returns a dict of DataFrames.
    """
    os.makedirs(save_dir, exist_ok=True)
    data = {}

    for ticker in tickers:
        print(f"Fetching {ticker}...")
        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
        df.index.name = "Date"
        df.to_csv(f"{save_dir}/{ticker}.csv")
        data[ticker] = df

    return data


def load_local_data(tickers, save_dir="../data/processed"):
    """Load previously saved CSVs instead of re-fetching from the API."""
    data = {}
    for ticker in tickers:
        path = f"{save_dir}/{ticker}.csv"
        df = pd.read_csv(path, index_col="Date", parse_dates=True, header=0, skiprows=[1,2])
        data[ticker] = df
    return data