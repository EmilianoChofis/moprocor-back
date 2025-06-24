from typing import List

from models.program_planning import ProgramPlanning, ProductionRun
from repositories.program_planning_repository import ProgramPlanningRepository


class ProgramPlanningService:
    @staticmethod
    async def get_by_week(week: int) -> ProgramPlanning:
        """
        Get all production runs for a specific week.
        :param week: The week number to filter by.
        :type week: int
        :return: List of ProgramPlanning documents for the specified week.
        :rtype: List[ProgramPlanning]
        """
        return await ProgramPlanningRepository.get_by_week(week)

    @staticmethod
    async def create_production_run(production_run: ProductionRun) -> ProductionRun:
        """
        Create a new production run.
        :param production_run: The production run data to create.
        :type production_run: ProductionRun
        :return: The created production run.
        :rtype: ProductionRun
        """
        return await ProgramPlanningRepository.create_production_run(production_run)
