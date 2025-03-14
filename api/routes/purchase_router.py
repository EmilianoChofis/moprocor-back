"""Define the purchase_router module"""
from typing import List

from fastapi import HTTPException, APIRouter, status

from models.purchase import Purchase
from services.purchase_service import PurchaseService

router = APIRouter()

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

@router.post("/createBundle", response_model=List[Purchase], status_code=status.HTTP_201_CREATED)
async def create_bundle(purchases: List[Purchase]):
    """Define the create_bundle function"""
    try:
        return await PurchaseService.create_bundle(purchases)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create bundle: {str(e)}",
        ) from e
