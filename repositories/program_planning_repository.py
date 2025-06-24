from typing import List

from beanie import PydanticObjectId

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

    @staticmethod
    async def update_production_run(run_id: PydanticObjectId, production_run: ProductionRun) -> ProductionRun:
        """
        Update an existing production run.
        :param run_id: The ID of the production run to update.
        :type run_id: PydanticObjectId
        :param production_run: The production run data to update.
        :type production_run: ProductionRun
        :return: The updated production run.
        :raises ValueError: If production run not found
        """
        production_run_old = await ProductionRun.get(run_id)
        if not production_run_old:
            raise ValueError(f"Production run with id {run_id} not found")

        # Convert the production run to dict excluding None values
        update_data = production_run.model_dump(exclude_none=True, exclude={'id'})

        # Update the document
        await production_run_old.update({"$set": update_data})

        # Fetch and return the updated document
        updated_run = await ProductionRun.get(run_id)
        if not updated_run:
            raise ValueError("Failed to retrieve updated production run")

        return updated_run

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
        production_run = await ProductionRun.get(run_id)
        if not production_run:
            raise ValueError(f"Production run with id {run_id} not found")

        # Delete the production run
        result = await production_run.delete()
        return result is not None