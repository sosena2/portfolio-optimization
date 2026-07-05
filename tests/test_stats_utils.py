import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pandas as pd
import numpy as np

from stats_utils import adf_test, calculate_var, calculate_sharpe_ratio


def test_adf_test_returns_expected_keys():
    np.random.seed(1)
    series = pd.Series(np.random.randn(200))
    result = adf_test(series, "test_series")
    assert "ADF Statistic" in result
    assert "p-value" in result
    assert "Stationary" in result
    assert isinstance(result["p-value"], float)


def test_adf_test_detects_stationary_series():
    np.random.seed(42)
    series = pd.Series(np.random.randn(500))  # white noise -> stationary
    result = adf_test(series, "white_noise")
    assert result["p-value"] < 0.05


def test_adf_test_detects_non_stationary_series():
    np.random.seed(42)
    series = pd.Series(np.random.randn(500).cumsum())  # random walk -> non-stationary
    result = adf_test(series, "random_walk")
    assert result["p-value"] > 0.05


def test_calculate_var_returns_a_float():
    np.random.seed(7)
    returns = pd.Series(np.random.normal(0, 0.02, 1000))
    var_95 = calculate_var(returns, confidence=0.95)
    assert isinstance(var_95, (float, np.floating))
    assert var_95 < 0  # VaR at 95% should be a negative (loss) value for normal returns


def test_calculate_sharpe_ratio_runs_without_error():
    np.random.seed(7)
    returns = pd.Series(np.random.normal(0.001, 0.02, 500))
    sharpe = calculate_sharpe_ratio(returns)
    assert isinstance(sharpe, (float, np.floating))
    assert not np.isnan(sharpe)