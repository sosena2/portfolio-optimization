import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pandas as pd
from data_loader import load_local_data


def test_load_local_data_reads_csv(tmp_path):
    save_dir = tmp_path / "processed"
    save_dir.mkdir()

    df = pd.DataFrame({
        "Adj Close": [100, 101, 102],
        "Close": [100, 101, 102],
        "High": [101, 102, 103],
        "Low": [99, 100, 101],
        "Open": [100, 101, 102],
        "Volume": [1000, 1100, 1200]
    }, index=pd.date_range("2024-01-01", periods=3))
    df.index.name = "Date"
    df.to_csv(save_dir / "TEST.csv")

    result = load_local_data(["TEST"], save_dir=str(save_dir))

    assert "TEST" in result
    assert not result["TEST"].empty
    assert "Adj Close" in result["TEST"].columns
    assert result["TEST"]["Adj Close"].iloc[0] == 100