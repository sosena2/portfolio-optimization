# Time Series Forecasting for Portfolio Management Optimization

## Overview

This project applies time series forecasting to historical financial data to support 
portfolio management decisions for **GMF Investments**. It covers data extraction, 
exploratory analysis, and forecasting models for three assets with different risk 
profiles: **TSLA** (high-growth stock), **BND** (bond ETF, low risk), and **SPY** 
(S&P 500 ETF, moderate risk).

Data covers **January 1, 2015 to June 30, 2026**, sourced via the YFinance API.

## Project Status

- ✅ **Task 1** — Data extraction, cleaning, EDA, stationarity testing, risk metrics (complete)
- 🔄 **Task 2** — Forecasting models (ARIMA complete, LSTM in progress)
- ⬜ Task 3 — Future forecasting & trend analysis
- ⬜ Task 4 — Portfolio optimization (MPT / Efficient Frontier)
- ⬜ Task 5 — Strategy backtesting

## Project Structure
portfolio-optimization/
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── unittests.yml
├── .gitignore
├── requirements.txt
├── README.md
├── data/
│   └── processed/         # Cached CSVs fetched from YFinance
├── notebooks/
│   ├── init.py
│   ├── README.md
│   └── eda_and_modeling.ipynb
├── src/
│   ├── init.py
│   ├── data_loader.py      # Fetch/load asset data
│   └── stats_utils.py      # ADF test, VaR, Sharpe Ratio helpers
├── tests/
│   ├── init.py
│   ├── test_data_loader.py
│   └── test_stats_utils.py
└── scripts/
└── init.py
## Setup

### 1. Clone the repo
```bash
git clone <repo-url>
cd portfolio-optimization
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the notebook
```bash
jupyter notebook notebooks/eda_and_modeling.ipynb
```

## Running Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v
```

Tests also run automatically via GitHub Actions on every push/PR (see 
`.github/workflows/unittests.yml`).

## What's Been Done

### Task 1 — Preprocess and Explore the Data
- Fetched historical OHLCV data for TSLA, BND, and SPY via `yfinance`
- Cleaned data: reindexed to business-day frequency, forward-filled missing values
- Combined adjusted close prices across all three assets into a single DataFrame
- Visualized closing prices, daily returns, and 30-day rolling volatility
- Detected outlier/extreme return days (>3 std dev)
- Ran Augmented Dickey-Fuller (ADF) tests on raw prices and daily returns:
  - Raw prices → non-stationary (as expected, given visible trends)
  - Daily returns → stationary, confirming `d=1` differencing is sufficient for ARIMA
- Calculated risk metrics: Value at Risk (95%) and annualized Sharpe Ratio for all 
  three assets

### Task 2 — Build Time Series Forecasting Models (in progress)
- Split TSLA closing price data chronologically (train: 2015–2024, test: 2025–2026)
- Built and fit an **ARIMA model** using `auto_arima` (pmdarima) for automatic 
  parameter selection
- Generated forecasts on the test period with confidence intervals
- Evaluated performance using MAE, RMSE, and MAPE
- **Next up**: LSTM model implementation and comparison against ARIMA baseline

## Key Insights So Far

- TSLA shows a strong long-term upward trend with the highest volatility of the 
  three assets; BND remains stable and low-volatility; SPY sits in between.
- TSLA's VaR (95%) is notably more negative than BND/SPY, reflecting larger 
  potential single-day losses.
- Daily returns across all assets are stationary, supporting the use of ARIMA-family 
  models with first-order differencing.

## Notes.
- Source data is fetched live via the YFinance API and cached locally in 
  `data/processed/`; it is not committed to version control.
