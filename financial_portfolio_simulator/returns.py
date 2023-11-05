from dataclasses import dataclass

import numpy as np


@dataclass
class Returns:
    stock_value: np.ndarray
    quantity_owned: np.ndarray

    def __len__(self):
        return len(self.stock_value)

    def __eq__(self, other):
        return (
            (len(self) == len(other))
            and (self.stock_value == other.stock_value).all()
            and (self.quantity_owned == other.quantity_owned).all()
        )

    @property
    def amount_invested(self) -> np.ndarray:
        return (self.units_transacted * self.stock_value).cumsum()

    @property
    def roi(self) -> np.ndarray:
        return self.countervalue / self.amount_invested

    @property
    def countervalue(self) -> np.ndarray:
        return self.quantity_owned * self.stock_value

    @property
    def units_transacted(self) -> np.ndarray:
        return np.diff(self.quantity_owned, prepend=0)

    @property
    def closing_roi(self) -> float:
        return self.roi[-1]


def calculate_returns(
    data: np.ndarray, strategy_label: str, strategy_settings: dict
) -> Returns:
    strategy = strategy_factory(strategy_label)(**strategy_settings)
    quantity_owned = strategy.compute_quantity_owned_over_time(data)
    return Returns(stock_value=data, quantity_owned=quantity_owned)


class LumpSumStrategy:
    def __init__(self, amount: float):
        self.amount = amount

    def compute_quantity_owned_over_time(self, stock_value: np.ndarray) -> Returns:
        return np.full_like(stock_value, self.amount / stock_value[0])


class CostAveragingStrategy:
    def __init__(
        self,
        recurring_amount: float,
        investing_frequency_days: int,
        number_of_purchases: int,
    ):
        self.recurring_amount = recurring_amount
        self.investing_frequency_days = investing_frequency_days
        self.number_of_purchases = number_of_purchases

    @property
    def days_between_purchases(self) -> int:
        return self.investing_frequency_days - 1

    def compute_quantity_owned_over_time(self, stock_value: np.ndarray) -> Returns:
        purchases = self._purchases()
        # Pad purhcases with zeros to match the length of stock_value
        purchases = self.align_purchases_length(stock_value, purchases)

        units_owned = purchases / stock_value
        return units_owned.cumsum()

    def align_purchases_length(self, stock_value, purchases):
        if len(purchases) < len(stock_value):
            purchases = np.pad(
                purchases,
                (0, len(stock_value) - len(purchases)),
                mode="constant",
                constant_values=0,
            )
        else:
            purchases = purchases[: len(stock_value)]
        return purchases

    def _purchases(self) -> np.ndarray:
        one_purchase_period = [self.recurring_amount] + [0] * (
            self.days_between_purchases
        )
        return np.tile(one_purchase_period, self.number_of_purchases)


def strategy_factory(strategy_label: str):
    strategies = {"lump_sum": LumpSumStrategy, "cost_averaging": CostAveragingStrategy}
    return strategies[strategy_label]
