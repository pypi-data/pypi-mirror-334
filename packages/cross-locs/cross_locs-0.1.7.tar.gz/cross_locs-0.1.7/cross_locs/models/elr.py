import pandera as pa
from pandera.typing import Series
from pandera.typing.geopandas import Geometry


class FullNetworkModel27700(pa.DataFrameModel):
    """
    - geometry: Geometry(crs=27700)
    - OBJECTID: int
    - ASSETID: int
    - L_SYSTEM: str
    - ELR: str
    - TRID: int
    - L_M_FROM: float
    - L_M_TO: float
    """

    geometry: Geometry(crs=27700)  # type: ignore
    OBJECTID: Series[int]
    ASSETID: Series[int]
    L_SYSTEM: Series[str]
    ELR: Series[str]
    TRID: Series[int]
    L_M_FROM: Series[float]
    L_M_TO: Series[float]


class DataframeWithElrMileages27700(pa.DataFrameModel):
    """
    All the new columns added to the original dataframe.
    ----------------------------------------------------
    - _elr: str
    - _mileage: float
    - _relative_mileage: float
    - _distance: float
    - _elr_exception: str
    - _message: str
    - _error: bool
    """

    _elr: Series[str] = pa.Field(nullable=True)
    _mileage: Series[float] = pa.Field(nullable=True)
    _relative_mileage: Series[float] = pa.Field(nullable=True)
    _distance: Series[float] = pa.Field(nullable=True)
    _elr_exception: Series[str] = pa.Field(nullable=True)
    _message: Series[str] = pa.Field(nullable=True)
    _error: Series[bool] = pa.Field(nullable=True)
