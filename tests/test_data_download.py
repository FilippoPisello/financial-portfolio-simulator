from datetime import date
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd

from financial_portfolio_simulator.dataset import YahooFinanceDataDownloader


def test_yahoo_finance_download_is_called_with_dates_as_str():
    downloader = YahooFinanceDataDownloader()
    with patch("yfinance.download") as mock_download:
        downloader.download(
            ticker="AAPL",
            start_date=date(2019, 1, 1),
            end_date=date(2019, 1, 31),
        )
        mock_download.assert_called_with(
            "AAPL", start="2019-01-01", end="2019-01-31", progress=False
        )


def test_yahoo_finance_raw_output_is_parsed_correctly():
    downloader = YahooFinanceDataDownloader()

    mock_download = Mock()
    mock_download.return_value = pd.DataFrame(
        {
            "Open": [1, 2, 3],
            "High": [4, 5, 6],
            "Low": [7, 8, 9],
            "Close": [10, 11, 12],
            "Adj Close": [13, 14, 15],
            "Volume": [16, 17, 18],
        }
    )
    with patch("yfinance.download", mock_download):
        result = downloader.download(
            ticker="AAPL",
            start_date=date(2019, 1, 1),
            end_date=date(2019, 1, 31),
        )
        assert (result == np.array([10, 11, 12])).all()
