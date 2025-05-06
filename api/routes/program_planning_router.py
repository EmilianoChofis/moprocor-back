
from typing import List

from fastapi import APIRouter, HTTPException, status

from models.program_planning import ProgramPlanning
from services.program_planning_service import ProgramPlanningService

router =  APIRouter()

@router.get("/getByWeek/{week}", response_model=ProgramPlanning)
async def get_production_runs_by_week(week: int):
    try:
        production_runs = await ProgramPlanningService.get_by_week(week)
        if not production_runs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No program planning found for week {week}",
            )
        return production_runs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve program planning: {str(e)}",
        ) from e
