from typing import List

from models.program_planning import ProgramPlanning
from models.program_planning import ProductionRun


class ProgramPlanningRepository:
    """
    Repository class for Program Planning data.
    """

    @staticmethod
    async def get_by_week(week: int) -> ProgramPlanning:
        """
        Get all production runs for a specific week.
        :param week: The week number to filter by.
        :type week: Int
        :return: List of ProgramPlanning documents for the specified week.
        :rtype: List[ProgramPlanning]
        """
        return await ProgramPlanning.find_one({"week_of_year": week})

    @staticmethod
    async def create_production_run(production_run: ProductionRun) -> ProductionRun:
        """
        Create a new production run.
        :param production_run: The production run data to create.
        :type production_run: ProductionRun
        :return: The created production run.
        :rtype: ProductionRun
        """
        return await ProductionRun.create(production_run)
