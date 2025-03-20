import geopandas as gpd
from typing import Any

from .constants import GeospatialConstants


class InputValidator:
    """Validates input data for ELR mileage calculations."""

    @staticmethod
    def validate_input_dataframe(gdf: gpd.GeoDataFrame, schema: Any) -> None:
        """
        Validates the input GeoDataFrame against requirements.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Input GeoDataFrame to validate
        schema : Any
            Schema to validate against

        Raises
        ------
        ValueError
            If validation fails
        """
        # Check for column conflicts
        for col in schema.__annotations__:
            if col in gdf.columns:
                raise ValueError(
                    f"Column {col} already exists in the GeoDataFrame - remove it for the function to operate."
                )

        # Check for geometry column
        if "geometry" not in gdf.columns:
            raise ValueError("Geometry column not found in the GeoDataFrame.")

        # Check CRS is 27700
        if gdf.crs is None or gdf.crs.to_epsg() != GeospatialConstants.REQUIRED_CRS:
            raise ValueError(
                f"GeoDataFrame CRS is not EPSG:{GeospatialConstants.REQUIRED_CRS}."
            )
