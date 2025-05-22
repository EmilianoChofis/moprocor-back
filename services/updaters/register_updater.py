"""
This module implements the RegisterUpdater class.
"""

from typing import Dict, Any

from config import logging
from services.updaters.base_updater import ProductionPlanUpdater
from services.ia_service import IAService
from repositories.program_planning_repository import ProgramPlanningRepository
from models.program_planning import ProgramPlanning


class RegisterUpdater(ProductionPlanUpdater):
    """
    Implementation of ProductionPlanUpdater for registering a new purchase.

    Input:
        - purchase: dict
        - box: dict
        - sheets: list[dict]
        - program_planning: dict (initially empty)
    Output:
        - program_planning: updated dict
    """

    def __init__(self, ia_service: IAService):
        """
        Initialize the RegisterUpdater with an IAService instance.

        Args:
            ia_service: The IAService instance to use for AI interactions.
        """
        self.ia_service = ia_service

    async def update(self, input_data: Dict[str, Any]) -> None:
        """
        Update the production plan based on the input data for a new purchase registration.

        Args:
            input_data: A dictionary containing:
                - purchase: Purchase data
                - box: Box data
                - sheets: List of available sheets
                - program_planning: Empty or initial program planning data
        """
        # Extract data from input
        purchase = input_data.get("purchase", {})
        box = input_data.get("box", {})
        sheets = input_data.get("sheets", [])
        program_planning = input_data.get("program_planning", {})

        # Get the week of the year from the purchase
        week_of_year = purchase.get("week_of_year")
        if not week_of_year:
            return

        # Generate prompt for AI
        prompt = self.ia_service.build_prompt(
            action_type="register",
            data={
                "purchase": purchase,
                "box": box,
                "sheets": sheets,
                "program_planning": program_planning,
            },
        )
        print("Prompt for AI:", prompt)
        # Call AI service
        ai_response = await self.ia_service.call(prompt)
        print("AI response:", ai_response)
        # Parse the response
        updated_program = self.ia_service.parse_response(ai_response)

        if not updated_program:
            return

        # Get existing program planning or create a new one
        program_planning = await ProgramPlanningRepository.get_by_week(week_of_year)
        if not program_planning:
            program_planning = ProgramPlanning(week_of_year=week_of_year)

        # Update program planning with AI response
        program_planning.production_runs = updated_program.get("production_runs", [])

        # Save the updated program planning
        await program_planning.save()
