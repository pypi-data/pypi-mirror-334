import numpy as np
from dataclasses import dataclass
from shapely.geometry import Point


@dataclass
class GeospatialConstants:
    """Constants for geospatial operations and coordinate handling."""

    # Points
    EMPTY_POINT: Point = Point()
    ZERO_POINT: Point = Point(0, 0)

    # Conditions for Erroneous Points
    NULL_COORDS_POINT: Point = Point(np.nan, np.nan)
    # Infinite coordinates are often marked as WRONG due to conversion of invalid ESPG:4326 coordinates to ESPG:27700 results in infinite values
    INFINITE_COORDS_POINT: Point = Point(np.inf, np.inf)
    # (1, 1) in EPSG:4326
    ORIGIN_COORDS_POINT: Point = Point(733_898.3258933355, -5_416_388.13814126)
    # (0, 0) in EPSG:4326
    ZERO_COORDS_POINT: Point = Point(622_575.7031043093, -5_527_063.8148287395)

    FAR_COORDS_THRESHOLD_M: float = 1_000  # 1km

    # Irish coordinates bounds in EPSG:27700
    IRISH_X_MIN: float = -203_722.42
    IRISH_X_MAX: float = 273_547.999
    IRISH_Y_MIN: float = 199_423.488
    IRISH_Y_MAX: float = 617_276.107

    # Coordinate Reference System we use here
    REQUIRED_CRS: int = 27700  # EPSG:27700
