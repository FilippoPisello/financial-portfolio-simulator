from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, timedelta
from random import randint

import numpy as np
import yfinance


@dataclass
class SimulationParameters:
    ticker: str
    start_date: date
    end_date: date


def generate_randomized_parameters(
    ticker: str,
    min_start_date: date,
    max_start_date: date,
    number_of_financial_periods: int,
) -> SimulationParameters:
    start_date = _generate_random_start_date(min_start_date, max_start_date)
    end_date = _calculate_end_date(start_date, number_of_financial_periods)
    return SimulationParameters(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
    )


def _generate_random_start_date(min_start_date: date, max_start_date: date) -> str:
    # Get the difference between the two dates in days
    delta = (max_start_date - min_start_date).days
    # Pick a random date in that range
    random_number_of_days = randint(0, delta)
    return min_start_date + timedelta(days=random_number_of_days)


def _calculate_end_date(start_date: date, number_of_financial_periods: int) -> str:
    return start_date + timedelta(days=7 * 4 * number_of_financial_periods)


class StockDataDownloader(ABC):
    @abstractmethod
    def download(self, ticker: str, start_date: date, end_date: date) -> np.ndarray:
        pass


class YahooFinanceDataDownloader(StockDataDownloader):
    def download(self, ticker: str, start_date: date, end_date: date) -> np.ndarray:
        str_start_date = start_date.strftime("%Y-%m-%d")
        str_end_date = end_date.strftime("%Y-%m-%d")
        df = yfinance.download(
            ticker, start=str_start_date, end=str_end_date, progress=False
        )
        return df["Close"].reset_index(drop=True).to_numpy()
