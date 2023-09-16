from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from random import randint


class StockDataDownloader(ABC):
    @abstractmethod
    def download(self, ticker, start_date, end_date):
        pass


def generate_datasets(
    downloader: StockDataDownloader,
    ticker: str,
    min_starting_date: str,
    max_starting_date: str,
    number_of_financial_periods: int,
    number_of_simulations: int,
) -> list[list[float]]:
    datasets = []
    for _ in range(number_of_simulations):
        start_date = _generate_random_start_date(min_starting_date, max_starting_date)
        end_date = _calculate_end_date(start_date, number_of_financial_periods)
        dataset = downloader.download(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )
        datasets.append(dataset)
    return datasets


def _generate_random_start_date(min_starting_date: str, max_starting_date: str) -> str:
    lower_limit = datetime.strptime(min_starting_date, "%Y-%m-%d")
    upper_limit = datetime.strptime(max_starting_date, "%Y-%m-%d")
    # Number of days between the two dates
    delta = (upper_limit - lower_limit).days
    random_number_of_days = randint(0, delta)
    # Add the random number of days to the lower limit
    random_date = lower_limit + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")


def _calculate_end_date(start_date: str, number_of_financial_periods: int) -> str:
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = start_date + timedelta(days=7 * 4 * number_of_financial_periods)
    return end_date.strftime("%Y-%m-%d")
