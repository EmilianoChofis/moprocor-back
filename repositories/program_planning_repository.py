from typing import List

from models.program_planning import ProgramPlanning


class ProgramPlanningRepository:
    """
    Repository class for Program Planning data.
    """

    @staticmethod
    async def get_by_week(week: int) -> List[ProgramPlanning]:
        """
        Get all production runs for a specific week.
        :param week: The week number to filter by.
        :type week: Int
        :return: List of ProgramPlanning documents for the specified week.
        :rtype: List[ProgramPlanning]
        """
        return await ProgramPlanning.find({"week_of_year": week}).to_list()