import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

def adf_test(series, series_name="Series"):
    """Run Augmented Dickey-Fuller test and return a readable summary dict."""
    series = series.dropna()
    result = adfuller(series)
    summary = {
        "series": series_name,
        "ADF Statistic": result[0],
        "p-value": result[1],
        "Critical Values": result[4],
        "Stationary": result[1] < 0.05
    }
    return summary


def calculate_var(returns, confidence=0.95):
    """Historical Value at Risk (VaR) at a given confidence level."""
    return np.percentile(returns.dropna(), (1 - confidence) * 100)


def calculate_sharpe_ratio(returns, risk_free_rate=0.02, periods_per_year=252):
    """Annualized Sharpe Ratio from daily returns."""
    excess_returns = returns.dropna() - (risk_free_rate / periods_per_year)
    return (excess_returns.mean() / excess_returns.std()) * np.sqrt(periods_per_year)