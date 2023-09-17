from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Self

import yaml

from financial_portfolio_simulator import CONFIG_DIR

CONFIG_PATH = CONFIG_DIR / "config.yml"


@dataclass
class ProjectConfig:
    ticker: str
    min_start_date: date
    max_start_date: date
    number_of_financial_periods: int
    strategies: dict[str, dict]
    number_of_simulations: int = 50

    @classmethod
    def sample_config(cls, **kwargs) -> Self:
        sample_input = {
            "ticker": "AAPL",
            "min_start_date": date(2019, 1, 1),
            "max_start_date": date(2019, 1, 31),
            "number_of_financial_periods": 26,
            "strategies": {
                "lump_sum": {
                    "amount": 1000,
                }
            },
        } | kwargs
        return cls(**sample_input)


def load_config() -> ProjectConfig:
    with open(CONFIG_PATH, "r") as f:
        config_dict = yaml.safe_load(f)
    config_dict["min_start_date"] = datetime.strptime(
        config_dict["min_start_date"], "%Y-%m-%d"
    ).date()
    config_dict["max_start_date"] = datetime.strptime(
        config_dict["max_start_date"], "%Y-%m-%d"
    ).date()
    return ProjectConfig(**config_dict)
