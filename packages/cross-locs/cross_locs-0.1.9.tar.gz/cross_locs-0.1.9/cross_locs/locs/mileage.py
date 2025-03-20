import geopandas as gpd
import pandas as pd


class MileageCalculator:
    """Handles mileage calculations for rail network points."""

    @staticmethod
    def adjust_mileage(gdf: gpd.GeoDataFrame) -> pd.Series:
        """
        Adjust mileage based on the geometry projection.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Input GeoDataFrame

        Returns
        -------
        pd.Series
            Adjusted mileage values
        """
        return gdf["_elr_geom"].project(
            gdf.geometry,
            normalized=True,
        )

    @staticmethod
    def find_absolute_mileage(*, start: float, end: float, dr: float) -> float:
        """
        Calculate absolute mileage of points using distance ratio and network model.

        Parameters
        ----------
        start : float
            Starting mileage point
        end : float
            Ending mileage point
        dr : float
            Distance ratio for the network model

        Returns
        -------
        float
            Absolute mileage value
        """
        sign = 1 if start < end else -1
        return start + sign * abs(start - end) * dr
