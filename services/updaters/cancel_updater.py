"""
This module implements the CancelUpdater class.
"""

from typing import Dict, Any

from services.updaters.base_updater import ProductionPlanUpdater
from services.ia_service import IAService
from repositories.program_planning_repository import ProgramPlanningRepository


class CancelUpdater(ProductionPlanUpdater):
    """
    Implementation of ProductionPlanUpdater for canceling a purchase.

    Input:
        - purchase: dict (the canceled purchase)
        - program_planning: dict (the program planning containing the purchase)
    Output:
        - program_planning: updated dict with the purchase removed
    """

    def __init__(self, ia_service: IAService):
        """
        Initialize the CancelUpdater with an IAService instance.

        Args:
            ia_service: The IAService instance to use for AI interactions.
        """
        self.ia_service = ia_service

    async def update(self, input_data: Dict[str, Any]) -> None:
        """
        Update the production plan based on the input data for a canceled purchase.

        Args:
            input_data: A dictionary containing:
                - purchase: Purchase data that has been canceled
                - program_planning: Program planning data containing the purchase
        """
        # Extract data from input
        purchase = input_data.get("purchase", {})
        program_planning = input_data.get("program_planning", {})

        # Get the week of the year from the purchase
        week_of_year = purchase.get("week_of_year")
        if not week_of_year:
            return

        # Generate prompt for AI
        prompt = self.ia_service.build_prompt(
            action_type="delete",
            data={"purchase": purchase, "program_planning": program_planning},
        )

        # Call AI service
        ai_response = await self.ia_service.call(prompt)

        # Parse the response
        updated_program = self.ia_service.parse_response(ai_response)

        if not updated_program:
            return

        # Get existing program planning
        program_planning_obj = await ProgramPlanningRepository.get_by_week(week_of_year)
        if not program_planning_obj:
            return

        # Update program planning with AI response
        program_planning_obj.production_runs = updated_program.get("production_runs", [])

        # Save the updated program planning
        await program_planning_obj.save()