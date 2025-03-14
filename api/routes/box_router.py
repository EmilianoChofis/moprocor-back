"""
Routes for box operations using MongoDB.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status

from models.box import Box
from services.box_service import BoxService

router = APIRouter()


@router.get("/getAll", response_model=List[Box])
async def get_boxes():
    """Define the get_boxes function"""
    try:
        return await BoxService.get_all_boxes()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve boxes: {str(e)}",
        ) from e


@router.get("/getBySymbol/{symbol}", response_model=Box)
async def get_box_by_symbol(symbol: str):
    """Define the get_box_by_symbol function"""
    box = await BoxService.get_box_by_symbol(symbol)
    if not box:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Box with symbol {symbol} not found",
        )
    return box


@router.post("/create", response_model=Box, status_code=status.HTTP_201_CREATED)
async def create_box(box: Box):
    """Define the create_box function"""
    try:
        return await BoxService.create_box(box)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create box: {str(e)}",
        ) from e
