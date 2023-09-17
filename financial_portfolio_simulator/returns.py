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
        # TODO: this will not work for strategies that invest more than once
        return self.quantity_owned * self.stock_value[0]

    @property
    def roi(self) -> np.ndarray:
        return self.countervalue / self.amount_invested

    @property
    def countervalue(self) -> np.ndarray:
        return self.quantity_owned * self.stock_value

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


def strategy_factory(strategy_label: str):
    strategies = {"lump_sum": LumpSumStrategy}
    return strategies[strategy_label]
