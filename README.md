# Time Series Forecasting for Portfolio Management Optimization

A GMF Investments project applying time series forecasting and Modern Portfolio Theory (MPT) to optimize
a portfolio across TSLA, BND, and SPY.

## Overview

This project analyzes historical financial data (Jan 2015 - Jun 2026) for three assets with distinct
risk profiles — Tesla (TSLA, high-growth/high-risk), Vanguard Total Bond Market ETF (BND, low-risk),
and the S&P 500 ETF (SPY, moderate-risk) — to forecast future price trends, construct an optimal
portfolio using Modern Portfolio Theory, and validate that portfolio through historical backtesting
against a standard 60/40 benchmark.

## Project Structure
portfolio-optimization/
├── .github/
│   └── workflows/
│       └── unittests.yml          # CI test runner
├── .vscode/
│   └── settings.json
├── data/
│   └── processed/                 # Cleaned CSVs, saved models, metrics (see Data section)
├── notebooks/
│   ├── eda_and_modeling.ipynb     # Task 1 (EDA) + Task 2 (ARIMA)
│   ├── lstm_model.ipynb           # Task 2 (LSTM)
│   ├── future_forecast.ipynb      # Task 3
│   ├── portfolio_optimization.ipynb  # Task 4
│   └── backtesting.ipynb          # Task 5
├── src/
│   ├── data_loader.py             # Fetch/load asset data from YFinance or local CSV
│   └── stats_utils.py             # Stationarity tests, risk metrics
├── tests/
│   ├── test_data_loader.py
│   └── test_stats_utils.py
├── requirements.txt
└── README.md
## Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Key dependencies: `yfinance`, `pandas`, `numpy`, `statsmodels`, `pmdarima`, `tensorflow`, `scikit-learn`,
`PyPortfolioOpt`, `matplotlib`.

## Data

Historical daily OHLCV data for TSLA, BND, and SPY (Jan 1, 2015 - Jun 30, 2026), sourced via `yfinance`
and cached locally as CSVs in `data/processed/`. Model binaries (`.keras`, `.pkl`) are excluded from
version control (see `.gitignore`); regenerate them by running the notebooks in order. Small JSON
result files (metrics, forecast/portfolio summaries) are committed since they're lightweight and used
to pass results between notebooks.

## Methodology by Task

### Task 1 — Data Preprocessing & EDA
*(`eda_and_modeling.ipynb`)*

- Fetched and cleaned historical price data for all three assets
- Analyzed closing price trends, daily returns, and rolling volatility
- Ran the Augmented Dickey-Fuller test to check stationarity of price levels vs. daily returns
- Calculated foundational risk metrics: Value at Risk (VaR) and historical Sharpe Ratio
- Identified and reviewed outlier return days

### Task 2 — Time Series Forecasting Models
*(`eda_and_modeling.ipynb` for ARIMA, `lstm_model.ipynb` for LSTM)*

- Split data chronologically (train: 2015-2024, test: 2025-2026) to preserve temporal order
- **ARIMA**: parameters selected via `auto_arima`, fitted on training data, forecasted over the test
  period
- **LSTM**: 60-day sliding window input, 2-layer LSTM architecture (64 → 32 units) with dropout
  regularization, trained with early stopping
- Compared both models using MAE, RMSE, and MAPE on the test set

| Model | Notes |
|-------|-------|
| ARIMA | Interpretable, produces native confidence intervals |
| LSTM  | Captures nonlinear patterns; confidence intervals approximated via Monte Carlo Dropout |

*(See `data/processed/lstm_metrics.json` and the ARIMA evaluation cell in `eda_and_modeling.ipynb` for
exact metric values.)*

### Task 3 — Future Forecasting
*(`future_forecast.ipynb`)*

- Generated a 12-month forward forecast for TSLA using the selected model (ARIMA)
- Visualized the forecast with 95% confidence intervals against historical prices

**Key results:**
- Projected 12-month change: **-44.26%**
- CI width: **83.89** (start of horizon) → **163.9** (end of horizon), a **1.95x** widening
- The point forecast shows a sharp initial decline that flattens toward ARIMA's long-run mean —
  a known limitation of ARIMA at longer horizons rather than a high-confidence directional prediction.
  The wide, persistent confidence interval reflects genuinely low reliability at this range, consistent
  with the Efficient Market Hypothesis's expectation that long-horizon price prediction is inherently
  difficult.

### Task 4 — Portfolio Optimization (MPT)
*(`portfolio_optimization.ipynb`)*

- Built an expected returns vector using TSLA's forecasted return (Task 3) and historical annualized
  returns for BND/SPY
- Computed the covariance matrix from historical daily returns
- Generated the Efficient Frontier using `PyPortfolioOpt`, identifying both the Max Sharpe (Tangency)
  and Minimum Volatility portfolios

| Portfolio | TSLA | BND | SPY | Return | Volatility | Sharpe |
|---|---|---|---|---|---|---|
| Min Volatility | 0% | 94.29% | 5.71% | -0.08% | 5.27% | -0.015 |
| **Max Sharpe (recommended)** | 0% | 0% | **100%** | **12.77%** | 17.72% | **0.721** |

**Recommendation:** Max Sharpe Portfolio (100% SPY). Both optimized portfolios excluded TSLA entirely,
a direct consequence of its deeply negative forecasted return — no diversification benefit justified
holding an asset with negative expected return. Between the remaining options, Max Sharpe offers
substantially better risk-adjusted return than Min Volatility, whose near-zero return provides
essentially no compensation for the risk taken.

*Note: this recommendation is highly sensitive to the Task 3 ARIMA forecast — a different model or
forecast horizon could shift TSLA's expected return enough to change the optimal allocation.*

### Task 5 — Strategy Backtesting
*(`backtesting.ipynb`)*

- Backtested the Task 4 recommended portfolio (Strategy) against a static 60% SPY / 40% BND benchmark
- Backtest window: Jan 2025 - Jun 2026 (held out from model training)

| Portfolio | Total Return | Annualized Return | Sharpe Ratio | Max Drawdown |
|---|---|---|---|---|
| Strategy (100% SPY) | 26.43% | 17.22% | 0.976 | -19.00% |
| Benchmark (60/40) | 16.89% | 11.15% | 0.999 | -11.67% |

**Conclusion:** The Strategy outperformed the Benchmark on absolute return (+6pp annualized) but not
on risk-adjusted return — its Sharpe ratio was marginally lower and its max drawdown notably deeper.
Since the optimizer excluded TSLA entirely, this backtest is effectively a comparison of SPY vs. a
SPY/BND blend rather than a genuine test of the forecasting pipeline's added value. Results should be
treated as inconclusive given the single backtest window, absence of transaction cost modeling, and the
sensitivity of the whole pipeline to Task 3's forecast uncertainty.

## Key Limitations

- Single backtest period; results may not generalize across different market regimes
- No transaction or rebalancing costs modeled
- TSLA forecast (and therefore portfolio composition) is highly sensitive to ARIMA's long-horizon
  reliability, which this project's own analysis shows is limited
- Per the Efficient Market Hypothesis, these models are best used as one input among many in a broader
  decision framework — not as standalone predictive tools

## Running the Project

Notebooks must be run in order, as later tasks depend on outputs from earlier ones:

1. `eda_and_modeling.ipynb` — Task 1 + ARIMA (Task 2)
2. `lstm_model.ipynb` — LSTM (Task 2), saves `lstm_metrics.json`
3. `future_forecast.ipynb` — Task 3, saves `forecast_summary.json`
4. `portfolio_optimization.ipynb` — Task 4, saves `portfolio_summary.json`
5. `backtesting.ipynb` — Task 5

## Tests

```powershell
pytest tests/
```
