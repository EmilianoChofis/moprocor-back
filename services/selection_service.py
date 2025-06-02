"""
Service classes for managing Sheet selections and Box wildcard lists.
"""

from typing import List, Optional
from beanie import PydanticObjectId

from models.selection import SheetsSelection, BoxWildcardList
from models.sheet import Sheet
from models.box import Box
from repositories.selection_repository import SheetsSelectionRepository, BoxWildcardRepository


class SelectionService:
    """Service for managing sheet selections and box wildcards."""

    def __init__(self):
        """Initialize the service with its repositories."""
        self.sheets_repo = SheetsSelectionRepository()
        self.box_repo = BoxWildcardRepository()

    async def get_current_sheet_selection(self) -> Optional[SheetsSelection]:
        """
        Get the current sheet selection with validation.

        :return: The current valid sheet selection or None.
        :rtype: Optional[SheetsSelection]
        """
        selection = await self.sheets_repo.get_current_selection()
        if not selection:
            return None

        # Validate that all sheets still exist
        for sheet_id in selection.sheet_ids:
            if not await Sheet.get(sheet_id):
                # Remove invalid IDs from the selection
                selection.sheet_ids.remove(sheet_id)

        return selection

    async def update_sheet_selection(
        self, sheet_ids: List[PydanticObjectId]
    ) -> SheetsSelection:
        """
        Update the sheet selection after validating the sheets exist.

        :param sheet_ids: List of Sheet IDs to include in the selection.
        :type sheet_ids: List[PydanticObjectId]
        :return: The updated SheetsSelection document.
        :rtype: SheetsSelection
        :raises ValueError: If any of the sheet IDs don't exist.
        """
        # Validate all sheets exist
        for sheet_id in sheet_ids:
            if not await Sheet.get(sheet_id):
                raise ValueError(f"Sheet with ID {sheet_id} not found")

        selection = SheetsSelection(sheet_ids=sheet_ids)
        return await self.sheets_repo.update_selection(selection)


    async def get_current_box_wildcards(self) -> Optional[BoxWildcardList]:
        """
        Get the current box wildcard list with validation.

        :return: The current valid box wildcard list or None.
        :rtype: Optional[BoxWildcardList]
        """
        wildcard_list = await self.box_repo.get_current_list()
        if not wildcard_list:
            return None

        # Validate that all boxes still exist
        for box_symbol in wildcard_list.box_symbols:
            if not await Box.find_one(Box.symbol == box_symbol):
                # Remove invalid symbols from the wildcard list
                wildcard_list.box_symbols.remove(box_symbol)

        return wildcard_list

    async def update_box_wildcards(
        self, box_symbols: List[str]
    ) -> BoxWildcardList:
        """
        Update the box wildcard list after validating the boxes exist.

        :param box_symbols: List of Box IDs to include in the wildcard list.
        :type box_symbols: List[PydanticObjectId]
        :return: The updated BoxWildcardList document.
        :rtype: BoxWildcardList
        :raises ValueError: If any of the box IDs don't exist.
        """
        # Validate all boxes exist based on their symbols
        for box_symbol in box_symbols:
            box = await Box.find_one(Box.symbol == box_symbol)
            if not box:
                raise ValueError(f"Box with symbol {box_symbol} not found")

        return await self.box_repo.update_wildcard_list(box_symbols)
