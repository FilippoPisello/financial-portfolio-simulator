from dataclasses import dataclass, field
from datetime import date, timedelta

import yfinance as yf


@dataclass
class StockHistory:
    """Represent the history of a stock price."""

    history: dict[date, float] = field(default_factory=dict)
    cursor: int = field(init=False, default=0)

    def move(self, days: int = 1) -> None:
        """Move the cursor forward by the specified number of days."""
        self.cursor += days

    def set_cursor_to(self, date: date) -> None:
        """Set the cursor to the specified date."""
        self.cursor = list(self.history.keys()).index(date)

    @property
    def current_value(self) -> float:
        """Return the value of the stock at the current date."""
        return self.history[self.current_date]

    @property
    def current_date(self) -> date:
        """Return the date pointed by the cursor."""
        return list(self.history.keys())[self.cursor]

    def get_price_n_days_ago(self, n: int) -> float:
        return self.history[self.current_date - timedelta(days=n)]


def download_stock_history(
    ticker: str, start_date: date, end_date: date
) -> StockHistory:
    """Download the history of a stock."""
    data = yf.download(ticker, start=start_date, end=end_date)
    return StockHistory(history=data["Close"].to_dict())
