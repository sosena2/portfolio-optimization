import os
from pathlib import Path

import pandas as pd

def fetch_asset_data(tickers, start_date, end_date, save_dir="../data/processed"):
    """
    Fetch historical OHLCV data for a list of tickers from YFinance.
    Saves each ticker's data as a separate CSV and returns a dict of DataFrames.
    """
    import yfinance as yf

    os.makedirs(save_dir, exist_ok=True)
    data = {}

    for ticker in tickers:
        print(f"Fetching {ticker}...")
        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
        df.index.name = "Date"
        df.to_csv(f"{save_dir}/{ticker}.csv")
        data[ticker] = df

    return data


def _read_local_csv(path):
    with open(path, "r", encoding="utf-8") as handle:
        first_line = handle.readline().strip()
        second_line = handle.readline().strip()

    if first_line.startswith("Price,") and second_line.startswith("Ticker,"):
        df = pd.read_csv(path, skiprows=[1, 2])
        if "Price" in df.columns:
            df = df.rename(columns={"Price": "Date"})
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date").sort_index()
        return df

    df = pd.read_csv(path, index_col="Date", parse_dates=True)
    return df.sort_index()


def load_local_data(tickers, save_dir="../data/processed"):
    """Load previously saved CSVs instead of re-fetching from the API."""
    data = {}
    for ticker in tickers:
        path = f"{save_dir}/{ticker}.csv"
        df = pd.read_csv(path, header=0, skiprows=[1, 2])
        df = df.rename(columns={df.columns[0]: "Date"})
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date").sort_index()
        data[ticker] = df
    return data