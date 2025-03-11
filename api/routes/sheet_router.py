"""
Routes for sheet operations using MongoDB.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status

from models.sheet import Sheet
from services.sheet_service import SheetService

router = APIRouter()


@router.get("/sheets", response_model=List[Sheet])
async def get_sheets():
    """Define the get_sheets function"""
    try:
        return await SheetService.get_all_sheets()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve sheets: {str(e)}",
        ) from e


@router.get("/sheets/{sheet_id}", response_model=Sheet)
async def get_sheet_by_id(sheet_id: str):
    """Define the get_sheet_by_id function"""
    sheet = await SheetService.get_sheet_by_id(sheet_id)
    if not sheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sheet with ID {sheet_id} not found",
        )
    return sheet

@router.post("/sheets", response_model=Sheet, status_code=status.HTTP_201_CREATED)
async def create_sheet(sheet: Sheet):
    """Define the create_sheet function"""
    try:
        return await SheetService.create_sheet(sheet)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create sheet: {str(e)}",
        ) from e

