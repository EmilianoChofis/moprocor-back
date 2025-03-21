"""Define the purchase_router module"""
import json
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
