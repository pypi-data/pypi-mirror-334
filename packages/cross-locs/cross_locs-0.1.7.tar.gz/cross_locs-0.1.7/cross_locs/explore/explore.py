import geopandas as gpd
from folium import Map


COLORS = [
    "red",
    "black",
    "blue",
    "cyan",
    "magenta",
    "purple",
    "orange",
    "brown",
    "pink",
    "gray",
    "olive",
    "navy",
    "teal",
    "maroon",
    "lime",
    "aqua",
    "fuchsia",
    "silver",
    "gold",
    "indigo",
    "violet",
]


def _validate_types(arg) -> None:
    if not isinstance(arg, gpd.GeoDataFrame):
        raise ValueError(
            f"One of your inputs is not a GeoDataFrame! {arg} is a {type(arg)}."
        )


def explore(*args: gpd.GeoDataFrame, **kwargs) -> Map:
    """
    Explores multiple GeoDataFrames on an interactive map.

    Parameters
    ----------
    *args : gpd.GeoDataFrame
        One or more GeoDataFrames to visualize.
    **kwargs : dict
        Optional keyword arguments:
    - colors : list of str
        - List of colors to use for each GeoDataFrame. Must be at least as long as the number of GeoDataFrames provided.

    Returns
    -------
    Map
        A folium.Map object with the GeoDataFrames plotted.

    Raises
    ------
    ValueError
        If any of the inputs is not a GeoDataFrame or if the number of colors provided is less than the number of GeoDataFrames.

    Notes
    -----
    This function uses the `explore` method of GeoDataFrame to visualize the data. If `colors` is not provided, it defaults to a predefined list of colors.
    """
    if not args:
        raise ValueError("Please provide at least one GeoDataFrame to explore.")

    for arg in args:
        _validate_types(arg)

    colors = kwargs.get("colors", COLORS)
    if len(colors) < len(args):
        raise ValueError(
            f"Please provide at least {len(args)} colors for each GeoDataFrame."
        )

    m = args[0].explore(color=colors[0])
    for arg, color in zip(args[1:], colors[1:]):
        m = arg.explore(m=m, color=color)

    return m
