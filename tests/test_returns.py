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


class TestCostAveragingStrategy:
    def test_the_recurring_amount_is_invested_every_x_trading_days(self):
        recurring_amount = 100

        result = calculate_returns(
            np.array([2, 2.5, 3, 3.5, 4]),
            "cost_averaging",
            {
                "recurring_amount": recurring_amount,
                "investing_frequency_days": 3,
                "number_of_purchases": 5,
            },
        )
        assert result.amount_invested[0] == recurring_amount
        assert result.amount_invested[1] == recurring_amount
        assert result.amount_invested[2] == recurring_amount
        assert result.amount_invested[3] == recurring_amount * 2

    def test_the_recurring_amount_is_purchased_only_n_times(self):
        recurring_amount = 100

        result = calculate_returns(
            np.array([2, 2.5, 3, 3.5, 4]),
            "cost_averaging",
            {
                "recurring_amount": recurring_amount,
                "investing_frequency_days": 2,
                "number_of_purchases": 1,
            },
        )
        assert (result.amount_invested == recurring_amount).all()

    def test_quantity_owned_depends_on_market_price_at_purchase(self):
        amount = 100

        result = calculate_returns(
            np.array([2, 2, 5, 5, 10, 10]),
            "cost_averaging",
            {
                "recurring_amount": amount,
                "investing_frequency_days": 2,
                "number_of_purchases": 3,
            },
        )
        assert result.quantity_owned[0] == amount / 2
        assert result.quantity_owned[1] == amount / 2
        assert result.quantity_owned[2] == (amount / 2) + (amount / 5)
        assert result.quantity_owned[3] == (amount / 2) + (amount / 5)
        assert result.quantity_owned[4] == (amount / 2) + (amount / 5) + (amount / 10)
        assert result.quantity_owned[5] == (amount / 2) + (amount / 5) + (amount / 10)
