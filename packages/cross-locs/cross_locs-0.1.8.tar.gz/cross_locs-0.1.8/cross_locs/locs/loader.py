import pickle
import numpy as np
import geopandas as gpd
from shapely.geometry import LineString


class ELRDataLoader:
    """Handles loading ELR reference data."""

    @staticmethod
    def load_elr_data(filepath: str) -> gpd.GeoDataFrame:
        """
        Load ELR reference data from pickle file.

        Parameters
        ----------
        filepath : str
            Path to the pickle file

        Returns
        -------
        gpd.GeoDataFrame
            Loaded ELR reference data

        Raises
        ------
        FileNotFoundError
            If the file doesn't exist
        """
        try:
            with open(filepath, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"ELR reference data file not found at {filepath}")

    @staticmethod
    def get_generic() -> gpd.GeoDataFrame:
        """
        Get generic ELR reference data. Used when no ELR reference data is available.
        It is neccessary to have SOME ELR reference data to complete the spatial join.

        Returns
        -------
        gpd.GeoDataFrame
            Default ELR reference data
        """
        generic_elr = gpd.GeoDataFrame(
            [
                {
                    "geometry": LineString([(0, 0), (1000, 1000)]),
                    "ELR": "INCORRECT_ELR_COORDS",
                    "TRID": np.nan,
                    "L_M_FROM": np.nan,
                    "L_M_TO": np.nan,
                }
            ],
            crs="EPSG:27700",
        )

        generic_elr.loc[:, "_elr_geom"] = generic_elr["geometry"]

        generic_elr = generic_elr.astype(
            {
                "ELR": "string",
                "TRID": "Int64",
                "L_M_FROM": "float64",
                "L_M_TO": "float64",
            }
        )

        return generic_elr
