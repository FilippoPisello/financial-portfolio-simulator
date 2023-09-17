from pathlib import Path

import numpy as np
import pandas as pd

from financial_portfolio_simulator.returns import Returns


def align_returns_length(returns: list[Returns]) -> list[Returns]:
    """Align the length of a list of Returns objects."""
    max_length = max(len(ret) for ret in returns)
    return [
        Returns(
            stock_value=np.pad(
                ret.stock_value,
                pad_width=(0, max_length - len(ret)),
                mode="edge",
            ),
            quantity_owned=np.pad(
                ret.quantity_owned,
                pad_width=(0, max_length - len(ret)),
                mode="edge",
            ),
        )
        for ret in returns
    ]


def compute_returns_statistics_over_time(returns: list[Returns]) -> pd.DataFrame:
    """Compute statistics over time for a list of Returns objects."""
    df = pd.concat(
        _compute_summary_statistics(
            values=np.array([ret.amount_invested for ret in returns]),
            label="Invested amount",
        )
        + _compute_summary_statistics(
            values=np.array([ret.countervalue for ret in returns]),
            label="Countervalue",
        )
        + _compute_summary_statistics(
            values=np.array([ret.roi for ret in returns]),
            label="ROI",
        ),
        axis=1,
    )
    df.index = [f"d{i}" for i in range(len(returns[0].amount_invested))]
    return df


def _compute_summary_statistics(values: np.array, label: str) -> list[pd.Series]:
    _min = pd.Series(values.min(axis=0), name=f"{label} | Min")
    _mean = pd.Series(values.mean(axis=0), name=f"{label} | Mean")
    _max = pd.Series(values.max(axis=0), name=f"{label} | Max")
    _sd = pd.Series(values.std(axis=0))
    _minus_2sd = pd.Series(_mean - 2 * _sd, name=f"{label} | -2sd")
    _plus_2sd = pd.Series(_mean + 2 * _sd, name=f"{label} | +2sd")
    return [_min, _minus_2sd, _mean, _plus_2sd, _max]


def save_dataframe_to_excel(df: pd.DataFrame, sheet_path: Path, tab_name: str):
    writer = pd.ExcelWriter(sheet_path, engine="openpyxl")
    df.to_excel(writer, sheet_name=tab_name)
    writer.close()
