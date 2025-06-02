"""
Repository classes for Sheet selection and Box wildcard lists.
"""

from typing import List, Optional
from beanie import PydanticObjectId
from models.selection import SheetsSelection, BoxWildcardList


class SheetsSelectionRepository:
    """Repository for managing sheet selections."""

    @staticmethod
    async def get_current_selection() -> Optional[SheetsSelection]:
        """
        Get the most recent sheet selection.

        :return: The most recent SheetsSelection document, or None if none exists.
        :rtype: Optional[SheetsSelection]
        """
        # Get the most recent selection by timestamp
        return await SheetsSelection.find_one()

    @staticmethod
    async def update_selection(selection: SheetsSelection) -> SheetsSelection:
        """
        Update or create the sheet selection, ensuring only one record exists.

        :param selection: The SheetsSelection document to save.
        :type selection: SheetsSelection
        :return: The saved SheetsSelection document.
        :rtype: SheetsSelection
        """
        # Delete any existing selections first
        await SheetsSelection.delete_all()
        # Save the new selection
        return await selection.save()


class BoxWildcardRepository:
    """Repository for managing box wildcard lists."""

    @staticmethod
    async def get_current_list() -> Optional[BoxWildcardList]:
        """
        Get the current box wildcard list.

        :return: The most recent BoxWildcardList document, or None if none exists.
        :rtype: Optional[BoxWildcardList]
        """
        return await BoxWildcardList.find_one()


    @staticmethod
    async def update_wildcard_list(box_symbols: List[str]) -> BoxWildcardList:
        """
        Update or create the box wildcard list, ensuring only one record exists.

        :param box_symbols: List of Box IDs to include in the wildcard list.
        :type box_symbols: List[PydanticObjectId]
        :return: The updated BoxWildcardList document.
        :rtype: BoxWildcardList
        """
        # Delete any existing wildcard lists first
        await BoxWildcardList.delete_all()
        # Create and save the new list
        new_list = BoxWildcardList(box_symbols=box_symbols)
        return await new_list.save()
