"""
Models for Sheet selection and Box wildcard lists.
"""

from datetime import datetime
from typing import List, Optional

from beanie import Document, PydanticObjectId


class SheetsSelection(Document):
    """Model for storing selected sheets for current work."""

    sheet_ids: List[PydanticObjectId]  # List of selected Sheet IDs

    class Settings:
        """Settings for the SheetsSelection model."""
        name = "sheets_selections"

    class Config:
        """Configuration for the SheetsSelection model."""
        json_schema_extra = {
            "example": {
                "sheet_ids": ["507f1f77bcf86cd799439011"],
            }
        }


class BoxWildcardList(Document):
    """Model for storing commonly reused box designs."""

    box_symbols: List[str]  # List of selected Box IDs

    class Settings:
        """Settings for the BoxWildcardList model."""
        name = "box_wildcards"

    class Config:
        """Configuration for the BoxWildcardList model."""
        json_schema_extra = {
            "example": {
                "box_symbols": ["DEGASA 04"],
            }
        }