"""
This module implements the DeliveryDateUpdater class.
"""

from typing import Dict, Any

from services.updaters.base_updater import ProductionPlanUpdater
from services.ia_service import IAService
from repositories.program_planning_repository import ProgramPlanningRepository


class DeliveryDateUpdater(ProductionPlanUpdater):
    """
    Implementation of ProductionPlanUpdater for updating delivery date.

    Input:
        - purchase: dict
        - programs: {
            - original_program_planning: dict,
            - new_program_planning: dict (may be empty if no week change)
          }
    Output:
        - programs: {
            - original_program_planning: updated dict,
            - new_program_planning: updated dict (if used)
          }
    """

    def __init__(self, ia_service: IAService):
        """
        Initialize the DeliveryDateUpdater with an IAService instance.

        Args:
            ia_service: The IAService instance to use for AI interactions.
        """
        self.ia_service = ia_service

    async def update(self, input_data: Dict[str, Any]) -> None:
        """
        Update the production plan based on the input data for a delivery date update.

        Args:
            input_data: A dictionary containing:
                - purchase: Purchase data with updated delivery date
                - programs: Dictionary containing original and possibly new program planning data
        """
        # Extract data from input
        purchase = input_data.get("purchase", {})
        programs = input_data.get("programs", {})

        original_program = programs.get("original_program_planning", {})
        new_program = programs.get("new_program_planning", {})

        # Get the original and new week of the year
        original_week = original_program.get("week_of_year")
        new_week = purchase.get("week_of_year")

        if not original_week:
            return

        # If the week has changed and new_program is empty, create a new program planning
        if new_week and new_week != original_week and not new_program:
            new_program = {"week_of_year": new_week, "production_runs": []}
            programs["new_program_planning"] = new_program

        # Generate prompt for AI
        prompt = self.ia_service.build_prompt(
            action_type="update_info",
            data={
                "purchase": purchase,
                "original_program_planning": original_program,
                "new_program_planning": new_program,
            },
        )

        # Call AI service
        ai_response = await self.ia_service.call(prompt)
        # Parse the response
        updated_programs = self.ia_service.parse_response(ai_response)

        if not updated_programs:
            return

        # Extraer el diccionario "programs" si existe en la respuesta
        programs_data = updated_programs.get("programs", updated_programs)

        # Update original program planning
        original_program_planning = await ProgramPlanningRepository.get_by_week(
            original_week
        )

        if original_program_planning and "original_program_planning" in programs_data:
            original_program_planning.production_runs = programs_data[
                "original_program_planning"
            ].get("production_runs", [])
            await original_program_planning.save()

        # Update new program planning if week changed
        if (
            new_week
            and new_week != original_week
            and "new_program_planning" in programs_data
        ):
            new_program_planning = await ProgramPlanningRepository.get_by_week(new_week)
            if not new_program_planning:
                from models.program_planning import ProgramPlanning

                new_program_planning = ProgramPlanning(week_of_year=new_week)

            new_program_planning.production_runs = programs_data[
                "new_program_planning"
            ].get("production_runs", [])
            await new_program_planning.save()
