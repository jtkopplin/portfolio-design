import yfinance as yf
import pandas as pd
from pathlib import Path

# Base directory is the folder where this script is run from (repo root)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

START_DATE = "2023-01-01"
END_DATE = "2023-12-31"

def fetch_data(ticker):
    """
    Fetch historical stock data from Yahoo Finance.
    """
    print(f"Fetching data for {ticker} from {START_DATE} to {END_DATE}...")
    data = yf.download(ticker, start=START_DATE, end=END_DATE)
    return data

def save_data(data, ticker):
    """
    Save DataFrame to /data/raw/ as CSV at the repo base level.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / f"{ticker}_data.csv"
    data.to_csv(file_path)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    ticker = input("Enter stock ticker: ").upper()
    df = fetch_data(ticker)
    save_data(df, ticker)


    for ticker in TICKER:
        data = fetch_data(ticker)
        save_data(data, ticker)