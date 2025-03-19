import pandas as pd

try:
    import pandas as _pd
    from vayu.pandas_utils import select_series, select_frame
    if not hasattr(_pd.DataFrame, "select"):
        _pd.DataFrame.select = select_frame
    if not hasattr(pd.Series, "select"):
        _pd.Series.select = select_series
except ImportError:
    pass
