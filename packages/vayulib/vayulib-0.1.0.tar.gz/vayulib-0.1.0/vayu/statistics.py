import numpy as np
import pandas as pd


def quantile(q) -> callable:
    """Return a function that computes the quantile of a series.

    Notes:
        - Helpful as an aggregation function.
        - About 2.5x faster than pandas.Series.quantile.
    """

    def inner(a):
        if isinstance(a, pd.Series):
            a = a.values
        if len(a) == 0:
            return np.nan
        return np.quantile(a, q)

    inner.__name__ = f"q{q}"

    return inner
