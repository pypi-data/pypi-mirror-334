try:
    import pandas as pd
    from plotly import graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    import plotly.io as pio
except ImportError:
    pd = None
    go = None
    make_subplots = None
    px = None
    pio = None


def _validate_libraries():
    if pd is None:
        raise ImportError("pandas is not installed. Please install pandas to use this function.")
    if None in [go, make_subplots, px, pio]:
        raise ImportError("plotly is not installed. Please install plotly to use this function.")


class Color:
    VERY_GREEN = "#26A69A"
    GREEN = "#B2DFDB"
    VERY_RED = "#EF5350"
    RED = "#FFCDD2"
    BG_YELLOW = "#FFFDEE"
    YELLOW_1 = "#f6c309"
    YELLOW_2 = "#fb9800"
    YELLOW_3 = "#fb6500"
    YELLOW_4 = "#f60c0c"


def line(
    series: pd.Series,
    index: pd.Series = None,
    name: str = None,
    width: float = 1,
    color: str = None,
    dash: str = None,
    shape: str = None,
    gl: bool = True,
    **kwargs,
):
    """Helper function to create line plots from a pandas series."""
    _validate_libraries()
    if index is not None:
        assert len(series) == len(index), "Series length should be equal to index length"

    line_dict = dict(width=width)
    if color is not None:
        line_dict["color"] = color
    if dash:
        line_dict["dash"] = dash
    if shape:
        line_dict["shape"] = shape
    kwargs = kwargs | dict(
        x=index if index is not None else series.index,
        y=series,
        mode=kwargs.get("mode", "lines"),
        name=name or series.name,
        line=line_dict if line_dict else None,
    )

    return go.Scattergl(**kwargs) if gl else go.Scatter(**kwargs)


def scatter(
    series: pd.Series,
    index: pd.Series = None,
    name: str = None,
    color: str = None,
    size: int = 10,
    symbol: str = "circle",
    gl: bool = True,
    **kwargs,
):
    """Helper function to create scatter plots from a pandas series."""
    _validate_libraries()
    dikt = dict(
        x=index if index is not None else series.index,
        y=series,
        mode="markers",
        name=name or series.name,
        marker_symbol=symbol,
        marker_size=size,
        marker_color=color,
    )
    kwargs = dikt | kwargs
    return go.Scattergl(**kwargs) if gl else go.Scatter(**kwargs)


def subplot(
    columns: int = 1,
    rows: int = 1,
    secondary: bool = True,
    shared_xaxes: bool = None,
    vertical_spacing: float = None,
    **kwargs,
):
    """Helper function to create subplots with secondary y-axis support."""
    _validate_libraries()
    return make_subplots(
        cols=columns,
        rows=rows,
        specs=[[{"secondary_y": secondary} for _ in range(columns)] for _ in range(rows)],
        shared_xaxes=shared_xaxes,
        vertical_spacing=vertical_spacing,
        **kwargs,
    )


def insert_title(
    fig,
    title,
    x=0.01,
    y=0.99,
    center: bool = False,
    size: int = 20,
    bgcolor: str = "rgba(255, 255, 255, 0.7)",
    color: str = "black",
    font_family: str = "Courier New, monospace",
):
    """Insert title in the figure."""

    _validate_libraries()
    fig.add_annotation(
        x=x,
        y=y,
        xref="paper",
        yref="paper",
        showarrow=False,
        text=title,
        font=dict(size=size, color=color, family=font_family),
        bgcolor=bgcolor,
        borderpad=2,
    )
    return fig
