from typing import List, Tuple, Union
import geopandas as gpd
import pandas as pd
import numpy as np

from .constants import GeospatialConstants


class CoordinateProcessor:
    """Processes and filters coordinates in a GeoDataFrame."""

    @staticmethod
    def filter_points_by_condition(
        gdf: gpd.GeoDataFrame,
        mask: Union[pd.Series, np.ndarray],
    ) -> List[int]:
        """
        Filter points by a specific condition.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Input GeoDataFrame
        mask : Union[pd.Series, np.ndarray]
            Boolean mask to filter rows in the GeoDataFrame.

        Returns
        -------
        List[int]
            List of row IDs matching the condition
        """
        return gdf[mask]["_id"].tolist()

    @staticmethod
    def process_special_coordinates(
        gdf: gpd.GeoDataFrame,
        mask: Union[pd.Series, np.ndarray],
    ) -> Tuple[gpd.GeoDataFrame, List[int]]:
        """
        Process points with special coordinate conditions.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Input GeoDataFrame
        mask : Union[pd.Series, np.ndarray]
            Boolean mask to filter rows in the GeoDataFrame.

        Returns
        -------
        Tuple[gpd.GeoDataFrame, List[int]]
            Modified GeoDataFrame and list of IDs for filtered points
        """
        matched_ids = CoordinateProcessor.filter_points_by_condition(gdf, mask)

        # Replace matched points with zero coordinates
        if matched_ids:
            gdf.loc[
                mask,
                ["geometry"],
            ] = GeospatialConstants.ZERO_POINT

        return gdf, matched_ids
