from datetime import date

from financial_portfolio_simulator.stock_history import StockHistory
from financial_portfolio_simulator.wallet import StockPosition


class LumpSumInvestmentStrategy:
    def __init__(self, stock_position: StockPosition, sum_to_invest: float) -> None:
        self.stock_position = stock_position
        self.sum_to_invest = sum_to_invest
        self.has_invested = False

    def trade(self, stock_history: StockHistory) -> None:
        if self.has_invested:
            return
        self.stock_position.buy_value(
            value=self.sum_to_invest,
            market_price=stock_history.current_value,
        )
        self.has_invested = True


class CostAveragingInvestmentStrategy:
    def __init__(self, stock_position: StockPosition, sum_to_invest: float) -> None:
        self.stock_position = stock_position
        self.sum_to_invest = sum_to_invest

    def trade(self, stock_history: StockHistory) -> None:
        if not self.is_first_working_day_of_month(stock_history.current_date):
            return
        self.stock_position.buy_value(self.sum_to_invest, stock_history.current_value)

    @staticmethod
    def is_first_working_day_of_month(date: date) -> bool:
        if date.weekday() in [5, 6]:
            return False
        if date.day == 1:
            return True
        if date.day > 3:
            return False
        if date.weekday() == 0:
            return True
        return False


class BiasedCostAveragingInvestmentStrategy:
    def __init__(
        self,
        stock_position: StockPosition,
        sum_to_invest: float,
        lookback_days: int = 14,
    ) -> None:
        self.stock_position = stock_position
        self.sum_to_invest = sum_to_invest
        self.lookback_days = lookback_days

    def trade(self, stock_history: StockHistory) -> None:
        if not self.is_first_working_day_of_month(stock_history.current_date):
            return
        amount_to_buy = self._compute_amount_to_buy(stock_history)
        self.stock_position.buy_value(
            value=amount_to_buy, market_price=stock_history.current_value
        )

    def _compute_amount_to_buy(self, stock_history: StockHistory) -> float:
        # If there is no history, buy the full amount
        try:
            reference_price = stock_history.get_price_n_days_ago(self.lookback_days)
        except KeyError:
            return self.sum_to_invest

        change = stock_history.current_value / reference_price - 1
        if change < -0.10:
            return self.sum_to_invest * 1.2
        if change < -0.05:
            return self.sum_to_invest * 1.1
        return self.sum_to_invest

    @staticmethod
    def is_first_working_day_of_month(date: date) -> bool:
        if date.weekday() in [5, 6]:
            return False
        if date.day == 1:
            return True
        if date.day > 3:
            return False
        if date.weekday() == 0:
            return True
        return False
