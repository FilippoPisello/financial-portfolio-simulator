from datetime import date
from unittest.mock import Mock

from financial_portfolio_simulator.__main__ import run_simulations
from financial_portfolio_simulator.config import ProjectConfig
from financial_portfolio_simulator.dataset import generate_randomized_parameters

SAMPLE_CONFIG = ProjectConfig(
    ticker="AAPL",
    min_start_date=date(2019, 1, 1),
    max_start_date=date(2019, 1, 31),
    number_of_financial_periods=2,
    strategies=["lump_sum"],
)


def test_download_function_is_called_as_many_times_as_the_number_of_simulations():
    downloader = Mock()
    config = ProjectConfig.sample_config(number_of_simulations=3)
    run_simulations(
        config=config,
        data_downloader=downloader,
    )
    assert downloader.download.call_count == config.number_of_simulations


def test_download_is_always_called_with_start_date_between_min_and_max_start_date():
    min_start_date = date(2019, 1, 1)
    max_start_date = date(2019, 1, 31)

    for _ in range(100):
        parmeters = generate_randomized_parameters(
            ticker="AAPL",
            min_start_date=min_start_date,
            max_start_date=max_start_date,
            number_of_financial_periods=2,
        )
        assert min_start_date <= parmeters.start_date <= max_start_date


def test_download_is_called_with_different_start_dates():
    """This test proves that the starting date is randomized."""
    start_dates = set()

    for _ in range(100):
        parmeters = generate_randomized_parameters(
            ticker="AAPL",
            min_start_date=date(2019, 1, 1),
            max_start_date=date(2019, 1, 31),
            number_of_financial_periods=2,
        )
        start_dates.add(parmeters.start_date)

    assert len(start_dates) > 1


def test_download_start_and_end_date_are_number_of_financial_periods_apart():
    number_of_financial_periods = 2
    for _ in range(100):
        parmeters = generate_randomized_parameters(
            ticker="AAPL",
            min_start_date=date(2019, 1, 1),
            max_start_date=date(2019, 1, 31),
            number_of_financial_periods=number_of_financial_periods,
        )
        duration = (parmeters.end_date - parmeters.start_date).days
        assert duration == 7 * 4 * number_of_financial_periods
