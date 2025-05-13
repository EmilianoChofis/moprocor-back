"""
This module implements the QuantityUpdater class.
"""

from typing import Dict, Any

from services.updaters.base_updater import ProductionPlanUpdater
from services.ia_service import IAService
from repositories.program_planning_repository import ProgramPlanningRepository


class QuantityUpdater(ProductionPlanUpdater):
    """
    Implementation of ProductionPlanUpdater for updating purchase quantity.
    
    Input:
        - purchase: dict
        - program_planning: dict
    Output:
        - program_planning: updated dict
    """
    
    def __init__(self, ia_service: IAService):
        """
        Initialize the QuantityUpdater with an IAService instance.
        
        Args:
            ia_service: The IAService instance to use for AI interactions.
        """
        self.ia_service = ia_service
    
    async def update(self, input_data: Dict[str, Any]) -> None:
        """
        Update the production plan based on the input data for a quantity update.
        
        Args:
            input_data: A dictionary containing:
                - purchase: Purchase data with updated quantity
                - program_planning: Current program planning data
        """
        # Extract data from input
        purchase = input_data.get("purchase", {})
        program_planning_data = input_data.get("program_planning", {})
        
        # Get the week of the year from the purchase
        week_of_year = purchase.get("week_of_year")
        if not week_of_year:
            return
        
        # Generate prompt for AI
        prompt = self.ia_service.build_prompt(
            action_type="update_quantity",
            data={
                "purchase": purchase,
                "program_planning": program_planning_data
            }
        )
        
        # Call AI service
        ai_response = await self.ia_service.call(prompt)
        
        # Parse the response
        updated_program = self.ia_service.parse_response(ai_response)
        
        if not updated_program:
            return
        
        # Get existing program planning
        program_planning = await ProgramPlanningRepository.get_by_week(week_of_year)
        if not program_planning:
            return
        
        # Update program planning with AI response
        program_planning.production_runs = updated_program.get("production_runs", [])
        
        # Save the updated program planning
        await program_planning.save()