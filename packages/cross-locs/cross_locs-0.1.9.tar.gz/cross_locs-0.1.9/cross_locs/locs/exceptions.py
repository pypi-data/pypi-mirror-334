from enum import Enum
from dataclasses import dataclass


@dataclass
class ExceptionInfo:
    """Information about ELR calculation exceptions."""

    code: str
    message: str
    ref: str = "https://docs.crosstech.co.uk/doc/violation-mileages-bAz6n1vCbB"


class ELRExceptionEnum(Enum):
    """Enumeration of possible ELR calculation exceptions."""

    FAR_COORDS = ExceptionInfo(
        "FAR_COORDS",
        "If the point's coordinates put it at over 1km away from its nearest relevant (ELR present on its corresponding track) it is considered far.",
    )
    INCORRECT_ELR_COORDS = ExceptionInfo(
        "INCORRECT_ELR_COORDS",
        "Submitted ELR is either incorrectly written or does not exist in the current Network Model.",
    )
    IRISH_COORDS = ExceptionInfo(
        "IRISH_COORDS",
        "The coordinates are in Ireland.",
    ) 
    EMPTY_COORDS = ExceptionInfo(
        "EMPTY_COORDS",
        "This case exists for cases when the input into the match() function is a Point() with no latitude or longitude specified.",
    )
    WRONG_COORDS = ExceptionInfo(
        "WRONG_COORDS",
        "If the coordinates of the point are not consistent with CRS ESPG:4326 then it would be considered WRONG. Practically this means that when the coordinate is translated to CRS ESPG:27700 it becomes infinite.",
    )
    ORIGIN_COORDS = ExceptionInfo(
        "ORIGIN_COORDS",
        "By convention whenever we don't know the coordinates of a point-like object we assign it coordinates of 1,1 in ESPG:4326. Points with such coordinates are considered to be at 'origin'.",
    )
    NULL_COORDS = ExceptionInfo(
        "NULL_COORDS",
        "If the coordinates of the point are null OR zero then it is considered NULL. When backend sends a point with null coordinates it is converted to 0 because we use float64 type, hence zero and null are treated equivalently.",
    )

    @property
    def code(self) -> str:
        return self.value.code

    @property
    def message(self) -> str:
        return self.value.message

    @property
    def ref(self) -> str:
        return self.value.ref
