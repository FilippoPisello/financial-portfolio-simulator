from dataclasses import dataclass


@dataclass
class StockPosition:
    """Represents a position on a single stock."""

    investment: float = 0
    units: float = 0

    def buy_units(self, units: float, market_price: float) -> None:
        self.units += units
        self.investment += units * market_price

    def buy_value(self, value: float, market_price: float) -> None:
        self.units += value / market_price
        self.investment += value

    @property
    def holding_price(self) -> float:
        return self.investment / self.units

    def countervalue(self, market_price: float) -> float:
        return self.units * market_price

    def return_on_investment(self, market_price: float) -> float:
        return market_price / self.holding_price - 1

    def copy(self):
        return StockPosition(self.investment, self.units)

    def is_empty(self):
        return self.investment == 0 and self.units == 0
