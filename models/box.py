"""
Box model for MongoDB.
"""

from typing import Optional
from pydantic import BaseModel
from beanie import Document, Indexed


# pylint: disable=too-many-ancestors
class Crease(BaseModel):
    """Crease model representing the crease dimensions of a box."""

    r1: Optional[float] = None  # Radius 1 of the crease
    r2: Optional[float] = None  # Radius 2 of the crease
    r3: Optional[float] = None  # Radius 3 of the crease


class Ink(BaseModel):
    """Inks model representing the inks used in the box."""

    gcmi_1: Optional[str] = None  # GCMI ink 1
    gcmi_2: Optional[str] = None  # GCMI ink 2
    gcmi_3: Optional[str] = None  # GCMI ink 3
    gcmi_4: Optional[str] = None  # GCMI ink 4


class Box(Document):
    """Box model representing a box document in MongoDB."""

    symbol: str = Indexed()  # Symbol of the box, indexed for faster queries
    ect: int  # Edge Crush Test value of the box
    liner: str  # Liner material of the box
    width: float  # Width of the box
    length: float  # Length of the box
    flute: str  # Flute type of the box
    treatment: bool  # Treatment type of the box
    client: str  # Client associated with the box
    creases: Crease  # Crease dimensions of the box
    inks: Ink  # Inks used in the box
    weight: Optional[float] = None  # Weight of the box
    status: str  # Status of the box (e.g., approved, pending, disabled)
    type: str  # Type of the extra information
    pdf_link: str = ""  # Link to the PDF document of the box

    # pylint: disable=too-few-public-methods
    class Settings:
        """Settings for the Box model."""

        name = "boxes"  # Collection name in MongoDB

    # pylint: disable=too-few-public-methods
    class Config:
        """Configuration for the Box model."""

        json_schema_extra = {
            "example": {
                "symbol": "DEG CR CE-10",
                "ect": 21,
                "liner": "kraft",
                "width": 55.8,
                "length": 150.3,
                "flute": "c",
                "treatment": False,
                "client": "degasa",
                "creases": {
                    "r1": 10,
                    "r2": 10,
                    "r3": 10,
                },
                "status": "APPROVED",
                "type": "CRR",
                "pdf_link": "DEG_CR_CE-10.pdf",
            }
        }
