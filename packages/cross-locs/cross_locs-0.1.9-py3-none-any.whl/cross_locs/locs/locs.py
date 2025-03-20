from pandera.typing import DataFrame
from typing import List, Dict
import geopandas as gpd
import pandera as pa
import pandas as pd
import numpy as np
import os

from .constants import GeospatialConstants
from .processor import CoordinateProcessor
from .exceptions import ELRExceptionEnum
from .mileage import MileageCalculator
from .validator import InputValidator
from .loader import ELRDataLoader

from ..models import DataframeWithElrMileages27700


class ELRMileageCalculationService:
    """Service class for calculating ELR mileages for geographic points."""

    def __init__(self, elrs: List[str] = None, trids: List[int] = None):
        """
        Initialize the service.
        """
        self.elrs = elrs
        self.trids = trids

        # Navigate via relative path to the ELR data file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.elr_data_path = os.path.join(current_dir, "..", "data", "elrs.pkl")

        self.constants = GeospatialConstants()

    def process_dataframe(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Process the input GeoDataFrame to calculate ELR mileages.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Input GeoDataFrame with geometries

        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame with calculated ELR mileages

        Raises
        ------
        ValueError
            If input validation fails
        """
        # Validate input
        InputValidator.validate_input_dataframe(gdf, DataframeWithElrMileages27700)

        # Add ID column for tracking
        gdf = gdf.copy()
        gdf.loc[:, "_id"] = range(len(gdf))

        # Process special coordinate cases
        special_point_ids = self._process_special_coordinates(gdf)

        # Save original geometry
        gdf.loc[:, "_saved_geom"] = gdf["geometry"]

        # Join with ELR data
        gdf = self._join_with_elr_data(gdf)

        # Restore original geometry (NOTE: sjoin changes the geometry column to the result of the join)
        gdf["geometry"] = gdf["_saved_geom"]

        # Calculate mileages
        gdf = self._calculate_mileages(gdf)

        # Apply filters and mark exceptions
        gdf = self._apply_filters(gdf, special_point_ids)

        # Format output
        gdf = self._format_output(gdf)

        return gdf

    def _process_special_coordinates(
        self, gdf: gpd.GeoDataFrame
    ) -> Dict[str, List[int]]:
        """
        Process all special coordinate cases.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Input GeoDataFrame

        Returns
        -------
        Dict[str, List[int]]
            Dictionary of special point IDs by category
        """
        processor = CoordinateProcessor
        constants = GeospatialConstants

        # Process null coordinates
        gdf, null_coords_ids = processor.process_special_coordinates(
            gdf,
            (gdf["geometry"] == constants.NULL_COORDS_POINT)
            | (gdf["geometry"] == constants.ZERO_COORDS_POINT),
        )

        # Process infinite coordinates
        gdf, infinite_coords_ids = processor.process_special_coordinates(
            gdf, gdf["geometry"] == constants.INFINITE_COORDS_POINT
        )

        # Process origin coordinates
        gdf, origin_coords_ids = processor.process_special_coordinates(
            gdf, gdf["geometry"] == constants.ORIGIN_COORDS_POINT
        )

        # Process empty coordinates
        gdf, empty_coords_ids = processor.process_special_coordinates(
            gdf, gdf["geometry"] == constants.EMPTY_POINT
        )

        # Process Irish assets
        gdf, irish_coords_ids = processor.process_special_coordinates(
            gdf,
            (
                (gdf.geometry.x > constants.IRISH_X_MIN)
                & (gdf.geometry.x < constants.IRISH_X_MAX)
                & (gdf.geometry.y > constants.IRISH_Y_MIN)
                & (gdf.geometry.y < constants.IRISH_Y_MAX)
            ),
        )

        return {
            "NULL_COORDS": null_coords_ids,
            "WRONG_COORDS": infinite_coords_ids,
            "ORIGIN_COORDS": origin_coords_ids,
            "EMPTY_COORDS": empty_coords_ids,
            "IRISH_COORDS": irish_coords_ids,
        }

    def _join_with_elr_data(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Join the input GeoDataFrame with ELR reference data.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Input GeoDataFrame

        Returns
        -------
        gpd.GeoDataFrame
            Joined GeoDataFrame

        Raises
        ------
        ValueError
            If geospatial join fails
        """
        # Load ELR reference data
        elrs = ELRDataLoader.load_elr_data(self.elr_data_path)

        # Filter ELRs
        if self.elrs is not None and len(self.elrs) > 0:
            elrs = elrs[elrs["ELR"].isin(self.elrs)]

        # Filter TRIDs
        if self.trids is not None and len(self.trids) > 0:
            elrs = elrs[elrs["TRID"].isin(self.trids)]

        if len(elrs) == 0:
            elrs = ELRDataLoader.get_generic()

        # Perform spatial join
        joined_gdf = gdf.sjoin_nearest(
            elrs,
            distance_col="_distance",
        )

        if len(joined_gdf) == 0:
            raise ValueError("Geospatial join failed to find any matches.")

        # Rename ELR column
        joined_gdf = joined_gdf.rename(columns={"ELR": "_elr"})

        return joined_gdf

    def _calculate_mileages(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Calculate relative and absolute mileages.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Input GeoDataFrame after joining with ELR data

        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame with calculated mileages
        """
        calculator = MileageCalculator

        # Calculate relative mileage
        gdf.loc[:, "_relative_mileage"] = calculator.adjust_mileage(gdf)

        # Calculate absolute mileage
        gdf.loc[:, "_mileage"] = gdf.apply(
            lambda x: calculator.find_absolute_mileage(
                start=x["L_M_FROM"],
                end=x["L_M_TO"],
                dr=x["_relative_mileage"],
            ),
            axis=1,
        )

        # Remove duplicate matches for the same point
        gdf = gdf.drop_duplicates(subset=["_id"], keep="first")

        return gdf

    def _apply_filters(
        self, gdf: gpd.GeoDataFrame, special_point_ids: Dict[str, List[int]]
    ) -> gpd.GeoDataFrame:
        """
        Apply filters and mark exceptions.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Input GeoDataFrame
        special_point_ids : Dict[str, List[int]]
            Dictionary of special point IDs by category

        Returns
        -------
        gpd.GeoDataFrame
            Filtered GeoDataFrame
        """
        processor = CoordinateProcessor
        const = GeospatialConstants

        # Process far points
        gdf, far_coords_ids = processor.process_special_coordinates(
            gdf,
            (gdf["_distance"] > const.FAR_COORDS_THRESHOLD_M)
            & (gdf.geometry != const.ZERO_POINT),
        )
        special_point_ids["FAR_COORDS"] = far_coords_ids

        # Process incorrect ELRs
        gdf, incorrect_elr_ids = processor.process_special_coordinates(
            gdf,
            gdf["_elr"] == ELRExceptionEnum.INCORRECT_ELR_COORDS.code,
        )
        special_point_ids["INCORRECT_ELR_COORDS"] = incorrect_elr_ids

        # Mark special coordinate points
        for enum in ELRExceptionEnum:
            exception_type = enum.code
            ids = special_point_ids.get(exception_type, [])

            if ids:
                gdf.loc[
                    gdf["_id"].isin(ids),
                    ["_elr", "_mileage"],
                ] = [exception_type, np.nan]

        return gdf

    def _format_output(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Format the output GeoDataFrame.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Input GeoDataFrame

        Returns
        -------
        gpd.GeoDataFrame
            Formatted GeoDataFrame
        """
        # Extract exception codes
        exception_codes = [e.name for e in ELRExceptionEnum]

        # Set _elr_exception column
        gdf.loc[:, "_elr_exception"] = gdf["_elr"].apply(
            lambda x: x if x in exception_codes else np.nan
        )

        # Clean up _elr column
        gdf["_elr"] = gdf["_elr"].apply(
            lambda x: x if x not in exception_codes else np.nan
        )

        # Set message and error columns
        gdf.loc[:, "_message"] = gdf["_elr_exception"].apply(
            lambda x: (
                f"{ELRExceptionEnum[x].message} Docs Reference: {ELRExceptionEnum[x].ref}"
                if not pd.isna(x)
                else np.nan
            )
        )

        gdf.loc[:, "_error"] = gdf["_elr_exception"].apply(
            lambda x: True if not pd.isna(x) else False
        )

        # Set the ZERO Points to EMPTY Points
        gdf.loc[gdf["geometry"] == GeospatialConstants.ZERO_POINT, "geometry"] = (
            GeospatialConstants.EMPTY_POINT
        )

        # Drop temporary columns
        gdf = gdf.drop(
            columns=[
                "index_right",
                "_id",
                "_elr_geom",
                "_saved_geom",
                "L_M_FROM",
                "L_M_TO",
            ]
        )

        # Rename TRID column
        gdf = gdf.rename(columns={"TRID": "_trid"})

        return gdf


@pa.check_types
def get_elr_mileages(
    gdf: gpd.GeoDataFrame,
    elrs: list[str] = None,
    trids: list[int] = None,
) -> DataFrame[DataframeWithElrMileages27700]:
    """
    Calculate ELR mileages for geographical points. It adds columns:

    - `_elr`: ELR code
    - `_trid`: TRID code
    - `_distance`: Distance to the nearest ELR
    - `_relative_mileage`: Relative mileage value
    - `_mileage`: Mileage value (in miles)
    - `_elr_exception`: Exception code
    - `_message`: Exception message
    - `_error`: Error flag

    ```python
    new_columns = [
        "_elr",
        "_trid",
        "_distance",
        "_relative_mileage",
        "_mileage",
        "_elr_exception",
        "_message",
        "_error",
    ]
    ```

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        Input GeoDataFrame with geometries in EPSG:27700

    elrs : list[str] (optional)
        List of ELRs to use for the calculation (eg. ["ECM1", "ECM2"])

    trids : list[int] (optional)
        List of TRIDs to use for the calculation (eg. [1001, 2001])

    Returns
    -------
    DataFrame[DataframeWithElrMileages27700]
        DataFrame with calculated ELR mileages

    Raises
    ------
    ValueError
        If validation fails or processing encounters errors
    """
    service = ELRMileageCalculationService(elrs, trids)
    return service.process_dataframe(gdf)
