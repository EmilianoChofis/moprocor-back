"""
Routes for sheet operations using MongoDB.
"""

from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Query

from models.sheet import Sheet
from services.sheet_service import SheetService

router = APIRouter()
ITEMS_PER_PAGE=10

@router.get("/getAll", response_model=List[Sheet])
async def get_sheets():
    """Define the get_sheets function"""
    try:
        return await SheetService.get_all_sheets()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve : {str(e)}",
        ) from e


@router.get("/getById/{sheet_id}", response_model=Sheet)
async def get_sheet_by_id(sheet_id: str):
    """Define the get_sheet_by_id function"""
    sheet = await SheetService.get_sheet_by_id(sheet_id)
    if not sheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sheet with ID {sheet_id} not found",
        )
    return sheet


@router.post("/create", response_model=Sheet, status_code=status.HTTP_201_CREATED)
async def create_sheet(sheet: Sheet):
    """Define the create_sheet function"""
    try:
        return await SheetService.create_sheet(sheet)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create sheet: {str(e)}",
        ) from e

@router.get("/getFilteredSheets", response_model=List[Sheet])
async def get_filtered_sheets(
    query: str = Query("", description="Filtro de búsqueda"),
    page: int = Query(1, description="Número de página")
):
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de página debe ser mayor a 0"
        )
    """Define the get_filtered_sheets function"""
    try:
        result = await SheetService.get_filtered_sheets(query, page, ITEMS_PER_PAGE)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve sheets: {str(e)}",
        ) from e

@router.get("/getPages", response_model=int)
async def get_pages(
    query: str = Query("", description="Filtro de búsqueda")
):
    """Define the get_pages function"""
    try:
        return await SheetService.get_pages(query, ITEMS_PER_PAGE)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve sheets: {str(e)}",
        ) from e

@router.put("/update/{sheet_id}", response_model=Sheet)
async def update_sheet(sheet_id: PydanticObjectId, update_data: dict):
    """
    Update a sheet by its ID.
    """
    try:
        return await SheetService.update_sheet(sheet_id, update_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update sheet: {str(e)}"
        )

@router.patch("/changeStatus/{sheet_id}", response_model=Sheet)
async def change_status(sheet_id: PydanticObjectId, sheet_status: str):
    """
    Change the status of a sheet by its ID.
    """
    try:
        return await SheetService.change_status(sheet_id, sheet_status)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change sheet status: {str(e)}"
        )