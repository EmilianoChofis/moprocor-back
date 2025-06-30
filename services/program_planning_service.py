from typing import List

from beanie import PydanticObjectId

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
        Create a new production run and associate it with the corresponding ProgramPlanning for its week.
        If no ProgramPlanning exists for that week, a new one will be created.
        
        :param production_run: The production run data to create.
        :type production_run: ProductionRun
        :return: The created production run.
        :rtype: ProductionRun
        """
        # Calculate the week of year from the scheduled_date
        week_of_year = production_run.scheduled_date.isocalendar()[1]
        
        # Create the production run first
        created_run = await ProgramPlanningRepository.create_production_run(production_run)
        
        # Check if a program planning exists for this week
        program_planning = await ProgramPlanningRepository.get_by_week(week_of_year)
        
        if program_planning:
            # Add the new production run to the existing program planning
            program_planning.production_runs.append(created_run)
            await program_planning.save()
        else:
            # Create a new program planning for this week with the production run
            program_planning = ProgramPlanning(
                production_runs=[created_run],
                week_of_year=week_of_year
            )
            await program_planning.save()
            
        return created_run

    @staticmethod
    async def update_production_run(run_id: PydanticObjectId, production_run: ProductionRun) -> ProductionRun:
        """
        Update an existing production run.
        :param production_run: The production run data to update.
        :type production_run: ProductionRun
        :return: The updated production run.
        :rtype: ProductionRun
        """
        return await ProgramPlanningRepository.update_production_run(run_id, production_run)

    @staticmethod
    async def delete_production_run(run_id: PydanticObjectId) -> bool:
        """
        Delete a production run by its ID.
        :param run_id: The ID of the production run to delete.
        :type run_id: PydanticObjectId
        :return: True if deletion was successful, False otherwise.
        :rtype: bool
        :raises ValueError: If production run not found
        """
        return await ProgramPlanningRepository.delete_production_run(run_id)