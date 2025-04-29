from typing import List, Dict, Any
from models.production_run import ProductionRun

from fastapi import APIRouter, status, HTTPException

from services.production_run_service import ProductionRunService

router = APIRouter()

@router.get("/getAll", response_model=List[ProductionRun])
async def get_all_production_runs():
    try:
        return await ProductionRunService.get_all_production_runs()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve production runs: {str(e)}",
        ) from e

@router.post("/getPlanFromIA", response_model=ProductionRun, status_code=status.HTTP_201_CREATED)
async def get_plan_from_ia(purchases: List[Dict[str, Any]], sheets: List[Dict[str, Any]], boxes: List[Dict[str, Any]]):
    try:
        return await ProductionRunService.get_plan_from_ia(purchases, sheets, boxes)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve plan from IA: {str(e)}",
        ) from e

@router.post("/createBundle", response_model=List[ProductionRun])
async def create_bundle_production_runs(
    production_runs: List[ProductionRun]
):
    try:
        result = await ProductionRunService.create_bundle_production_runs(
            production_runs
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No production runs were created.",
            )

        return {
            "message": "Production runs created successfully",
            "production_runs": result,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create production runs: {str(e)}",
        ) from e