from datetime import datetime
from unittest.mock import Mock

from financial_portfolio_simulator.dataset import generate_datasets


def test_download_function_is_called_as_many_times_as_the_number_of_simulations():
    downloader = Mock()
    generate_datasets(
        downloader=downloader,
        ticker="AAPL",
        min_starting_date="2019-01-01",
        max_starting_date="2019-01-03",
        number_of_financial_periods=2,
        number_of_simulations=3,
    )
    assert downloader.download.call_count == 3


def test_number_of_datasets_returned_is_equal_to_the_number_of_simulations():
    downloader = Mock()
    downloader.download.return_value = [1, 2, 3]

    datasets = generate_datasets(
        downloader=downloader,
        ticker="AAPL",
        min_starting_date="2019-01-01",
        max_starting_date="2019-01-03",
        number_of_financial_periods=2,
        number_of_simulations=3,
    )
    assert len(datasets) == 3


def test_download_is_always_called_with_start_date_between_min_and_max_starting_date():
    downloader = Mock()
    min_date = "2019-01-01"
    max_date = "2019-01-03"

    generate_datasets(
        downloader=downloader,
        ticker="AAPL",
        min_starting_date=min_date,
        max_starting_date=max_date,
        number_of_financial_periods=2,
        number_of_simulations=100,
    )
    for call in downloader.download.call_args_list:
        start_date = call[1]["start_date"]
        assert start_date >= min_date
        assert start_date <= max_date


def test_download_is_called_with_different_starting_dates():
    """This test proves that the starting date is randomized."""
    downloader = Mock()
    generate_datasets(
        downloader=downloader,
        ticker="AAPL",
        min_starting_date="2019-01-01",
        max_starting_date="2019-01-03",
        number_of_financial_periods=2,
        number_of_simulations=50,
    )
    start_dates = {call[1]["start_date"] for call in downloader.download.call_args_list}
    assert len(start_dates) > 1


def test_download_start_and_end_date_are_always_4_times_the_number_of_financial_periods_apart():
    downloader = Mock()
    number_of_financial_periods = 2
    generate_datasets(
        downloader=downloader,
        ticker="AAPL",
        min_starting_date="2019-01-01",
        max_starting_date="2019-01-03",
        number_of_financial_periods=number_of_financial_periods,
        number_of_simulations=50,
    )
    for call in downloader.download.call_args_list:
        start_date = datetime.strptime(call[1]["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(call[1]["end_date"], "%Y-%m-%d")
        assert (end_date - start_date).days == 7 * 4 * number_of_financial_periods
