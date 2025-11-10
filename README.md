# Portfolio Design

A Python-based portfolio management and analysis tool for fetching, analyzing, and optimizing financial data.

## Overview

This project provides tools for collecting historical stock market data and performing portfolio analysis. Currently in early development, the project includes data fetching capabilities from Yahoo Finance with plans to expand into portfolio optimization, risk analysis, and backtesting.

## Features

- Fetch historical stock data from Yahoo Finance
- Store data in CSV format for easy analysis
- Configurable date ranges and data parameters
- Robust error handling and logging

## Project Structure

```
portfolio-design/
├── src/                    # Source code
│   └── fetch_data.py      # Data fetching utilities
├── data/                   # Data storage
│   ├── raw/               # Raw CSV data files
│   └── trading_data.db    # SQLite database
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd portfolio-design
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Fetching Stock Data

Run the data fetching script interactively:

```bash
python src/fetch_data.py
```

When prompted, enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL).

The script will:
- Download historical data from Yahoo Finance
- Save it to `data/raw/{TICKER}_data.csv`

### Current Data

The repository includes sample data for:
- **AAPL** (Apple Inc.) - 2023 data
- **BABA** (Alibaba Group) - 2023 data
- **SPY** (S&P 500 ETF) - 2023 data (in SQLite database)

## Configuration

The fetch_data.py script uses the following default settings:
- **Date Range**: January 1, 2023 - December 31, 2023
- **Output Directory**: `data/raw/`

These can be modified by editing the constants in the script or through configuration files (planned feature).

## Dependencies

- **yfinance**: Yahoo Finance API wrapper for fetching market data
- **pandas**: Data manipulation and analysis

See `requirements.txt` for version requirements.

## Development Roadmap

### Planned Features

- [ ] Portfolio optimization algorithms
- [ ] Risk metrics and analysis
- [ ] Backtesting framework
- [ ] Interactive visualization dashboard
- [ ] Multiple data source support
- [ ] Configuration file support
- [ ] Command-line interface (CLI)
- [ ] Unit tests and CI/CD pipeline
- [ ] Jupyter notebooks for analysis
- [ ] Real-time data streaming

## Data Sources

- **Yahoo Finance**: Historical stock prices, volumes, and fundamentals

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Submit a pull request

## License

[Add license information here]

## Disclaimer

This software is for educational and research purposes only. It is not financial advice. Always do your own research and consult with financial professionals before making investment decisions.
