"""Define the purchase_router module"""
import json
from typing import List

from fastapi import HTTPException, APIRouter, status, Query

from models.purchase import Purchase
from services.purchase_service import PurchaseService

router = APIRouter()
ITEMS_PER_PAGE=10

@router.get("/getAll", response_model=List[Purchase])
async def get_purchases():
    """Define the get_purchases function"""
    try:
        return await PurchaseService.get_all_purchases()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve : {str(e)}",
        ) from e


@router.post("/createBundle", status_code=status.HTTP_201_CREATED)
async def create_bundle(purchases: List[Purchase]):
    """Define the create_bundle function"""
    try:
        inserted_count, json_purchases, json_boxes, json_sheets = await PurchaseService.create_bundle(purchases)

        return {
            "message": "Purchases created successfully",
            "count": inserted_count,
            "purchases": json.loads(json_purchases) if json_purchases else {},
            "boxes": json.loads(json_boxes) if json_boxes else {},
            "sheets": json.loads(json_sheets) if json_sheets else {}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create bundle: {str(e)}",
        ) from e

@router.get("/getFilteredPurchases", response_model=List[Purchase])
async def get_filtered_purchases(
query: str = Query("", description="Filtro de búsqueda"),
    page: int = Query(1, description="Número de página")
):
    """Define the get_filtered_purchases function"""
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de página debe ser mayor a 0"
        )

    try:
        result = await PurchaseService.get_filtered_purchases(query, page, ITEMS_PER_PAGE)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve filtered purchases: {str(e)}",
        ) from e

@router.get("/getPages", response_model=int)
async def get_pages(
        query: str = Query("", description="Filtro de búsqueda")
):
    """Obtiene el total de páginas"""
    try:
        return await PurchaseService.get_pages(query, ITEMS_PER_PAGE)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve total pages: {str(e)}"
        ) from e

