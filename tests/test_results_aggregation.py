import numpy as np
import pandas as pd

from financial_portfolio_simulator.returns import Returns
from financial_portfolio_simulator.statistics import (
    align_returns_length,
    compute_returns_statistics_over_time,
)


def test_if_returns_have_different_lenghts_they_are_aligned():
    returns = [
        Returns(
            stock_value=np.array([10, 20, 30]),
            quantity_owned=np.array([1, 1, 1]),
        ),
        Returns(
            stock_value=np.array([10, 30]),
            quantity_owned=np.array([1, 1]),
        ),
    ]

    actual = align_returns_length(returns)

    expected = [
        Returns(
            stock_value=np.array([10, 20, 30]),
            quantity_owned=np.array([1, 1, 1]),
        ),
        Returns(
            stock_value=np.array([10, 30, 30]),
            quantity_owned=np.array([1, 1, 1]),
        ),
    ]
    assert actual == expected


def test_if_only_one_iteration_summary_statistics_are_the_values_themselves():
    returns = [
        Returns(
            stock_value=np.array([10, 20, 30]),
            quantity_owned=np.array([1, 1, 1]),
        )
    ]

    actual = compute_returns_statistics_over_time(returns)

    expected = pd.DataFrame(
        {
            "Invested amount | Min": [10, 10, 10],
            "Invested amount | -2sd": [10, 10, 10],
            "Invested amount | Mean": [10, 10, 10],
            "Invested amount | +2sd": [10, 10, 10],
            "Invested amount | Max": [10, 10, 10],
            "Countervalue | Min": [10, 20, 30],
            "Countervalue | -2sd": [10, 20, 30],
            "Countervalue | Mean": [10, 20, 30],
            "Countervalue | +2sd": [10, 20, 30],
            "Countervalue | Max": [10, 20, 30],
            "ROI | Min": [1, 2, 3],
            "ROI | -2sd": [1, 2, 3],
            "ROI | Mean": [1, 2, 3],
            "ROI | +2sd": [1, 2, 3],
            "ROI | Max": [1, 2, 3],
        },
        index=[f"d{i}" for i in range(3)],
    )
    pd.testing.assert_frame_equal(actual, expected, check_dtype=False)


def test_if_multiple_iterations_summary_statistics_computed_properly():
    returns = [
        Returns(
            stock_value=np.array([10, 20, 30]),
            quantity_owned=np.array([1, 1, 1]),
        ),
        Returns(
            stock_value=np.array([10, 30, 60]),
            quantity_owned=np.array([1, 1, 1]),
        ),
    ]

    actual = compute_returns_statistics_over_time(returns)

    expected = pd.DataFrame(
        {
            "Invested amount | Min": [10, 10, 10],
            "Invested amount | -2sd": [10, 10, 10],
            "Invested amount | Mean": [10, 10, 10],
            "Invested amount | +2sd": [10, 10, 10],
            "Invested amount | Max": [10, 10, 10],
            "Countervalue | Min": [10, 20, 30],
            "Countervalue | -2sd": [10, 15, 15],
            "Countervalue | Mean": [10, 25, 45],
            "Countervalue | +2sd": [10, 35, 75],
            "Countervalue | Max": [10, 30, 60],
            "ROI | Min": [1, 2, 3],
            "ROI | -2sd": [1, 1.5, 1.5],
            "ROI | Mean": [1, 2.5, 4.5],
            "ROI | +2sd": [1, 3.5, 7.5],
            "ROI | Max": [1, 3, 6],
        },
        index=[f"d{i}" for i in range(3)],
    )
    pd.testing.assert_frame_equal(actual, expected, check_dtype=False)
