from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from models.program_planning import ProgramPlanning, ProductionRun
from services.program_planning_service import ProgramPlanningService

router = APIRouter()


@router.get("/getByWeek/{week}", response_model=ProgramPlanning)
async def get_production_runs_by_week(week: int):
    try:
        production_runs = await ProgramPlanningService.get_by_week(week)
        if not production_runs:
            return ProgramPlanning(
                production_runs=[],
                week_of_year=week,
            )
        return production_runs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al carga programa: {str(e)}",
        ) from e


@router.post("/create/production_run", response_model=ProductionRun)
async def create_production_run(production_run: ProductionRun):
    try:
        created_production_run = await ProgramPlanningService.create_production_run(
            production_run
        )
        return created_production_run
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la corrida producción: {str(e)}",
        ) from e

@router.put("update/production_run/{run_id}", response_model=ProductionRun)
async def update_production_run(run_id: PydanticObjectId, production_run: ProductionRun):
    try:
        updated_production_run = await ProgramPlanningService.update_production_run(
            run_id, production_run
        )
        return updated_production_run
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la producción: {str(e)}",
        ) from e

@router.delete("/delete/production_run/{run_id}", response_model=bool)
async def delete_production_run(run_id: PydanticObjectId):
    try:
        result = await ProgramPlanningService.delete_production_run(run_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la corrida de producción: {str(e)}",
        ) from e