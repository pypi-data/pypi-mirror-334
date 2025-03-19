import math
from datetime import datetime
from operator import attrgetter
from pathlib import Path
from typing import Optional, Hashable, Union, Tuple

from vayu.common import Interval
from vayu.time import TimeWindow, from_timestamp

try:
    import pandas as pd

    DayOfWeek = pd.CategoricalDtype(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ordered=True
    )
except ImportError:
    pd = None
    DayOfWeek = None


def _validate_libraries():
    if pd is None:
        raise ImportError("pandas is not installed. Please install pandas to use this function.")


def concat_frame_from_dir(
    path, prefix: str = None, extension="parquet", progress=False
) -> pd.DataFrame:
    """Concatenate all dataframes in a directory"""

    path = Path(path)
    files = path.glob(f"*.{extension}")
    if prefix is not None:
        files = [f for f in files if f.name.startswith(prefix)]
    files = sorted(files, key=attrgetter("name"))
    reader_func = None
    match extension:
        case "feather":
            reader_func = pd.read_feather
        case "csv":
            reader_func = pd.read_csv
        case "pickle":
            reader_func = pd.read_pickle
        case "parquet":
            reader_func = pd.read_parquet

    frags = []
    n = len(files)
    for i, f in enumerate(files):
        frags.append(reader_func(f))
        if progress:
            print(f"Finished reading [{i + 1}/{n}] {f.name}")

    return pd.concat([f for f in frags if not f.empty], ignore_index=True)


def slice_frame(
    interval: Interval,
    df: "pd.DataFrame",
    level: Optional[int] = None,
    key: Optional[Hashable] = None,
    axis=0,
    exclude: bool = False,
) -> "pd.DataFrame":
    """Slice a dataframe using this interval.

    Args:
        interval: The interval to slice
        df: The dataframe to slice.
        level: The index or column level to slice on
        key: The row index or column to slice on to slice on
        axis: The axis to slice on (0 for index, 1 for columns)
        exclude: If True, exclude the interval instead of including it

    Notes:
        - If key is not specified, the level (or index if level is None) should be sorted in increasing order
        - If neither key nor level is specified, the 0th level of index is used for sliced on.
    """
    _validate_libraries()
    if level is not None:
        slicer = [slice(None)] * df.index.nlevels
        slicer[level] = slice(interval.start, interval.end)
        slicer = pd.IndexSlice[tuple(slicer)]
    elif key is not None:
        key = df[key] if axis == 0 else df.loc[key]
        slicer = (interval.start <= key) & (key <= interval.end)
    else:
        slicer = pd.IndexSlice[interval.start: interval.end]

    if isinstance(df, pd.DataFrame):
        sliced = df.loc[slicer, :] if axis == 0 else df.loc[:, slicer]
        if exclude:
            sliced = (
                df.loc[df.index.difference(sliced.index), :]
                if axis == 0
                else df.loc[:, df.columns.difference(sliced.columns)]
            )
    else:
        sliced = df.loc[slicer]
        if exclude:
            sliced = df.loc[df.index.difference(sliced.index)]

    return sliced


def is_frame_empty(df: Optional[Union["pd.DataFrame", "pd.Series"]]) -> bool:
    """Check if a dataframe is empty."""
    return df is None or len(df) == 0


def get_frame_window(
    df: "pd.DataFrame", column: str = None, level: int = 0
) -> Optional[TimeWindow]:
    """Get the time window of a dataframe.

    Args:
        df: dataframe
        column: If specified, the window is computed from the min and max of the column.
        level: Window is computed from the min and max of the index at the specified level.

    """
    _validate_libraries()
    if is_frame_empty(df):
        return None
    if column:
        start_time, end_time = df[column].min(), df[column].max()
    else:
        start_time, end_time = df.index.min(), df.index.max()
        if isinstance(start_time, tuple):
            start_time, end_time = start_time[level], end_time[level]

    return TimeWindow(from_timestamp(start_time.timestamp()), from_timestamp(end_time.timestamp()))


def split_frame(
    obj: Union["pd.Series", "pd.DataFrame"], n: Optional[Union[int, float, datetime]] = 0.5
) -> Union[Tuple["pd.Series", "pd.Series"], Tuple["pd.DataFrame", "pd.DataFrame"]]:
    """Split a dataframe or series into two parts.

    Args:
        obj: The object to split
        n: The index to split at. If float, it is treated as a fraction of the length of the object.
           If int, it is treated as an index.
           If datetime, it is treated as a timestamp.

    Returns:
        A tuple of two objects, the first part and the second part.
    """
    _validate_libraries()
    if isinstance(n, float):
        assert abs(n) <= 1, "Float split index should be less than equal to 1"
        n = math.floor(len(obj) * n)
    if isinstance(n, int):
        return obj.iloc[:n], obj.iloc[n:]
    else:
        return obj.loc[:n], obj.loc[n:]


def select_frame(frame: "pd.DataFrame", **conditions):
    """Select rows from a dataframe based on conditions."""
    _validate_libraries()
    for key, condition in conditions.items():
        parts = key.split("__")
        if len(parts) == 1:
            parts.append("eq")
        key, op = parts
        if isinstance(condition, Interval):
            frame = slice_frame(condition, frame, key=key, exclude=op in ("neq", "ne"))
        else:
            frame = frame[_selector(frame[key], op, condition)]
    return frame


def select_series(series: "pd.Series", **conditions):
    _validate_libraries()
    for op, condition in conditions.items():
        if isinstance(condition, Interval):
            series = series[(condition.start <= series) & (series <= condition.end)]
        else:
            series = series[_selector(series, op, condition)]
    return series


def _selector(series: "pd.Series", op, condition) -> "pd.Series":
    _validate_libraries()
    match op:
        case "eq":
            return series == condition
        case "ne" | "neq":
            return series != condition
        case "gt":
            return series > condition
        case "gte":
            return series >= condition
        case "lt":
            return series < condition
        case "lte":
            return series <= condition
        case "in" | "isin":
            return series.isin(condition)
        case "nin" | "notin":
            return ~series.isin(condition)
        case "isna" | "isnull":
            return series.isna() if condition else series.notna()
