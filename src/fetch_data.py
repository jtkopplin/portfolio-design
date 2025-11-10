import yfinance as yf
import pandas as pd
from pathlib import Path
import logging
import sys
from datetime import datetime
import configparser

# Base directory is the folder where this script is run from (repo root)
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.ini"

def load_config():
    """
    Load configuration from config.ini file.

    Returns:
        dict: Configuration parameters with defaults
    """
    config = configparser.ConfigParser()

    # Default configuration
    defaults = {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31',
        'data_directory': 'data/raw',
        'log_file': 'logs/fetch_data.log',
        'log_level': 'INFO',
        'show_progress': False,
        'timeout': 30
    }

    # Try to read config file
    if CONFIG_FILE.exists():
        try:
            config.read(CONFIG_FILE)

            # Extract values from config file
            if 'DATA' in config:
                defaults['start_date'] = config.get('DATA', 'start_date', fallback=defaults['start_date'])
                defaults['end_date'] = config.get('DATA', 'end_date', fallback=defaults['end_date'])
                defaults['data_directory'] = config.get('DATA', 'data_directory', fallback=defaults['data_directory'])

            if 'LOGGING' in config:
                defaults['log_file'] = config.get('LOGGING', 'log_file', fallback=defaults['log_file'])
                defaults['log_level'] = config.get('LOGGING', 'log_level', fallback=defaults['log_level'])

            if 'FETCHING' in config:
                defaults['show_progress'] = config.getboolean('FETCHING', 'show_progress', fallback=defaults['show_progress'])
                defaults['timeout'] = config.getint('FETCHING', 'timeout', fallback=defaults['timeout'])

        except Exception as e:
            print(f"Warning: Error reading config file, using defaults: {e}")

    return defaults

# Load configuration
CONFIG = load_config()

# Set up paths
DATA_DIR = BASE_DIR / CONFIG['data_directory']
LOG_FILE = BASE_DIR / CONFIG['log_file']

# Ensure log directory exists
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, CONFIG['log_level'].upper(), logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Date range from config
START_DATE = CONFIG['start_date']
END_DATE = CONFIG['end_date']

def validate_ticker(ticker):
    """
    Validate ticker symbol format.

    Args:
        ticker (str): Stock ticker symbol

    Returns:
        bool: True if valid, False otherwise
    """
    if not ticker or not isinstance(ticker, str):
        return False

    # Remove whitespace and check length
    ticker = ticker.strip()
    if len(ticker) < 1 or len(ticker) > 10:
        return False

    # Check for valid characters (letters, numbers, dots, hyphens)
    if not all(c.isalnum() or c in ['.', '-'] for c in ticker):
        return False

    return True

def fetch_data(ticker):
    """
    Fetch historical stock data from Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol

    Returns:
        pd.DataFrame: Historical stock data or None if error occurs
    """
    try:
        logger.info(f"Fetching data for {ticker} from {START_DATE} to {END_DATE}...")

        # Download data with configurable progress display
        data = yf.download(ticker, start=START_DATE, end=END_DATE, progress=CONFIG['show_progress'])

        # Check if data was retrieved
        if data.empty:
            logger.error(f"No data found for ticker '{ticker}'. Please verify the ticker symbol is correct.")
            return None

        logger.info(f"Successfully fetched {len(data)} rows of data for {ticker}")
        return data

    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

def save_data(data, ticker):
    """
    Save DataFrame to /data/raw/ as CSV at the repo base level.

    Args:
        ticker (str): Stock ticker symbol
        data (pd.DataFrame): Stock data to save

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Data directory verified: {DATA_DIR}")

        # Create file path
        file_path = DATA_DIR / f"{ticker}_data.csv"

        # Save to CSV
        data.to_csv(file_path)
        logger.info(f"Data saved successfully to {file_path}")

        # Log file size
        file_size = file_path.stat().st_size
        logger.info(f"File size: {file_size:,} bytes")

        return True

    except PermissionError:
        logger.error(f"Permission denied: Cannot write to {DATA_DIR}")
        return False
    except Exception as e:
        logger.error(f"Error saving data for {ticker}: {str(e)}")
        return False

def main():
    """Main function to run the data fetching process."""
    try:
        # Log configuration info
        logger.info(f"Configuration loaded - Date range: {START_DATE} to {END_DATE}")
        logger.info(f"Data will be saved to: {DATA_DIR}")

        # Get ticker input
        ticker = input("Enter stock ticker: ").strip().upper()

        # Validate ticker
        if not validate_ticker(ticker):
            logger.error(f"Invalid ticker symbol: '{ticker}'. Please enter a valid ticker (1-10 alphanumeric characters).")
            sys.exit(1)

        logger.info(f"Validated ticker: {ticker}")

        # Fetch data
        df = fetch_data(ticker)

        if df is None or df.empty:
            logger.error("Failed to fetch data. Exiting.")
            sys.exit(1)

        # Save data
        success = save_data(df, ticker)

        if not success:
            logger.error("Failed to save data. Exiting.")
            sys.exit(1)

        logger.info("Data fetch and save completed successfully!")

    except KeyboardInterrupt:
        logger.warning("\nProcess interrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()