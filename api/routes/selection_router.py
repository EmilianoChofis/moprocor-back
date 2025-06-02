"""
API routes for managing Sheet selections and Box wildcard lists.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId

from models.selection import SheetsSelection, BoxWildcardList
from services.selection_service import SelectionService

router = APIRouter(
    prefix="/api/selections",
    tags=["selections"],
    responses={404: {"description": "Not found"}},
)

selection_service = SelectionService()


@router.get("/sheets/current", response_model=Optional[SheetsSelection])
async def get_current_sheet_selection():
    """
    Get the current sheet selection.
    :return: The current sheet selection or None.
    """
    return await selection_service.get_current_sheet_selection()


@router.post("/sheets", response_model=SheetsSelection)
async def create_sheet_selection(sheet_ids: List[PydanticObjectId]):
    """
    Create a new sheet selection.

    :param sheet_ids: List of Sheet IDs to include in the selection.
    :return: The created sheet selection.
    """
    try:
        return await selection_service.update_sheet_selection(sheet_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/boxes/wildcards/current", response_model=Optional[BoxWildcardList])
async def get_current_box_wildcards():
    """
    Get the current box wildcard list.

    :return: The current box wildcard list or None.
    """
    return await selection_service.get_current_box_wildcards()


@router.post("/boxes/wildcards", response_model=BoxWildcardList)
async def update_box_wildcards(box_symbols: List[str]):
    """
    Update the box wildcard list.

    :param box_symbols: List of Box IDs to include in the wildcard list.
    :return: The updated box wildcard list.
    """
    try:
        return await selection_service.update_box_wildcards(box_symbols)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

