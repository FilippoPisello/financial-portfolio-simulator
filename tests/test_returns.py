import numpy as np

from financial_portfolio_simulator.returns import calculate_returns


class TestLumpSumStrategy:
    def test_the_entire_amount_is_invested_at_t0_and_then_held(self):
        amount_to_invest = 1000
        result = calculate_returns(
            np.array([2, 2.5, 3]),
            "lump_sum",
            {"amount": amount_to_invest},
        )
        assert result.amount_invested[0] == amount_to_invest
        assert result.amount_invested[1] == amount_to_invest
        assert result.amount_invested[2] == amount_to_invest

    def test_the_quantity_is_always_equal_to_amount_divided_by_the_price_at_t0(
        self,
    ):
        amount_to_invest = 1000
        result = calculate_returns(
            np.array([2, 2.5, 3]),
            "lump_sum",
            {"amount": amount_to_invest},
        )
        assert result.quantity_owned[0] == amount_to_invest / 2
        assert result.quantity_owned[1] == amount_to_invest / 2
        assert result.quantity_owned[2] == amount_to_invest / 2

    def test_countervalue_is_amount_invested_times_price_change(self):
        amount_to_invest = 1000
        result = calculate_returns(
            np.array([2, 2.5, 3]),
            "lump_sum",
            {"amount": amount_to_invest},
        )
        assert result.countervalue[0] == amount_to_invest
        assert result.countervalue[1] == amount_to_invest * 2.5 / 2
        assert result.countervalue[2] == amount_to_invest * 3 / 2
