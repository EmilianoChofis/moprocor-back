"""
Model for the sheet table
"""

from typing import List, Optional

from beanie import Document


class Sheet(Document):
    """Sheet model representing a sheet document in MongoDB."""

    roll_width: int
    p1: int
    p2: int
    p3: int
    ect: List[int]
    grams: float
    description: Optional[str] = ""
    boxes: Optional[List[str]] = []  # List of Box objects associated with the sheet
    speed: int
    status: bool = True
    available_meters: Optional[int] = 0

    class Settings:
        """Settings for the Sheet model."""

        name = "sheets"

    class Config:
        """Configuration for the Sheet model."""

        json_schema_extra = {
            "example": {
                "roll_width": 133,
                "p1": 110,
                "p2": 110,
                "p3": 110,
                "ect": [19],
                "grams": 389,
                "description": "This is a description",
                "boxes": [
                    {"symbol": "box_001"},
                ],
                "speed": 80,
                "status": True,
                "available_meters": 0
            }
        }
