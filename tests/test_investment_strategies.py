from datetime import date, timedelta
from unittest.mock import MagicMock

from financial_portfolio_simulator.investment_strategies import (
    BiasedCostAveragingInvestmentStrategy,
    CostAveragingInvestmentStrategy,
    LumpSumInvestmentStrategy,
)
from financial_portfolio_simulator.stock_history import StockHistory
from financial_portfolio_simulator.wallet import StockPosition


class TestLumpSumInvestmentStrategy:
    def test_strategy_buys_on_first_day(self):
        strategy = LumpSumInvestmentStrategy(MagicMock(), sum_to_invest=100)

        strategy.trade(StockHistory({date(2023, 1, 1): 100}))

        strategy.stock_position.buy_value.assert_called_with(
            value=100, market_price=100
        )

    def test_no_purchases_are_made_after_the_first_one(self):
        strategy = LumpSumInvestmentStrategy(MagicMock(), sum_to_invest=100)

        history = StockHistory({date(2023, 1, 1): 100})
        strategy.trade(history)
        history.add(date(2023, 1, 2), 200)
        strategy.trade(history)

        strategy.stock_position.buy_value.assert_called_once_with(
            value=100, market_price=100
        )


class TestCostAveragingInvestmentStrategy:
    def test_strategy_buys_on_first_working_day_of_the_month(self):
        strategy = CostAveragingInvestmentStrategy(StockPosition(), sum_to_invest=100)

        first_working_day_jan_2023 = date(2023, 1, 2)
        strategy.trade(StockHistory({first_working_day_jan_2023: 100}))

        assert strategy.stock_position.units == 1
        assert strategy.stock_position.investment == 100

    def test_strategy_does_not_buy_in_any_other_day_of_the_month(self):
        strategy = CostAveragingInvestmentStrategy(StockPosition(), sum_to_invest=100)
        for day in [1] + list(range(3, 32)):
            strategy.trade(StockHistory({date(2023, 1, day): 100}))
        assert strategy.stock_position.is_empty()


class TestBiasedCostAveragingInvestmentStrategy:
    def test_strategy_buys_on_first_working_day_of_the_month(self):
        strategy = BiasedCostAveragingInvestmentStrategy(MagicMock(), sum_to_invest=100)

        first_working_day_jan_2023 = date(2023, 1, 2)
        strategy.trade(StockHistory({first_working_day_jan_2023: 100}))

        strategy.stock_position.buy_value.assert_called_with(
            value=100, market_price=100
        )

    def test_strategy_does_not_buy_in_any_other_day_of_the_month(self):
        strategy = BiasedCostAveragingInvestmentStrategy(MagicMock(), sum_to_invest=100)
        for day in [1] + list(range(3, 32)):
            strategy.trade(StockHistory({date(2023, 1, day): 100}))
        strategy.stock_position.buy_value.assert_not_called()

    def test_if_stock_dropped_5_percent_or_more_then_buy_10_percent_more(self):
        strategy = BiasedCostAveragingInvestmentStrategy(
            MagicMock(), sum_to_invest=100, lookback_days=14
        )

        first_working_day_jan_2023 = date(2023, 1, 2)
        two_weeks_before = first_working_day_jan_2023 - timedelta(days=14)
        reference_price = 10
        current_price = reference_price * (1 - 0.05)
        strategy.trade(
            StockHistory(
                {
                    two_weeks_before: reference_price,
                    first_working_day_jan_2023: current_price,
                }
            )
        )

        strategy.stock_position.buy_value.assert_called_with(
            value=100 * 1.1, market_price=current_price
        )
