from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class StockHistory:
    history: dict[date, float] = field(default_factory=dict)

    def add(self, date: date, value: float) -> None:
        self.history[date] = value

    @property
    def latest_value(self) -> float:
        return self.history[max(self.history.keys())]

    @property
    def latest_date(self) -> date:
        return max(self.history.keys())

    def get_price_n_days_ago(self, n: int) -> float:
        return self.history[self.latest_date - timedelta(days=n)]
