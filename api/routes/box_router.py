"""
Routes for box operations using MongoDB.
"""

from typing import List, Dict, Union
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query

from models.box import Box
from services.box_service import BoxService

router = APIRouter()
ITEMS_PER_PAGE=6

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
async def create_box(box: Box, pdf_file: UploadFile = File(...)):
    """Define the create_box function"""
    try:
        return await BoxService.create_box(box,  pdf_file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create box: {str(e)}",
        ) from e

@router.get("/getFilteredBoxes", response_model=List[Box])
async def get_filtered_boxes(
    query: str = Query("", description="Filtro de búsqueda"),
    page: int = Query(1, description="Número de página")
):
    """Obtiene las cajas con paginación"""
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de página debe ser mayor a 0"
        )

    try:
        result = await BoxService.get_filtered_boxes(query, page, ITEMS_PER_PAGE)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve boxes: {str(e)}"
        )

@router.get("/getPages", response_model=Dict[str, int])
async def get_pages(
        query: str = Query("", description="Filtro de búsqueda")
):
    """Obtiene el total de páginas"""
    try:
        total_pages = await BoxService.get_pages(query, ITEMS_PER_PAGE)
        return {"total_pages": total_pages}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve total pages: {str(e)}"
        )
