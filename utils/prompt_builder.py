"""
This module implements the PromptBuilder class for constructing AI prompts.
"""

import json
import os
from typing import Dict, Any


class PromptBuilder:
    """
    Builds prompts for AI by combining base instructions, specific instructions, and domain data.
    """
    
    def __init__(self):
        """Initialize the PromptBuilder."""
        self.base_instructions = self._load_base_instructions()
        self.specific_instructions = {
            "register": "This prompt refers to a registration of a new purchase. "
                       "You need to create an optimal production plan for this new purchase.",
            "update_quantity": "This prompt refers to updating the quantity of an existing purchase. "
                              "You need to adjust the production plan to accommodate the new quantity.",
            "update_delivery_date": "This prompt refers to updating the delivery date of an existing purchase. "
                                   "You need to adjust the production plan to accommodate the new delivery date, "
                                   "which may involve moving the purchase to a different week."
        }
    
    def _load_base_instructions(self) -> str:
        """
        Load the base instructions from the template file.
        
        Returns:
            str: The base instructions.
        """
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            template_path = os.path.join(current_dir, "templates", "base_instructions.json")
            
            with open(template_path, "r", encoding="utf-8") as file:
                instructions = json.load(file)
                return instructions.get("base_rules", "You are an expert in optimizing production plans...")
        except Exception as e:
            # Fallback to default instructions if file cannot be loaded
            return "You are an expert in optimizing production plans for corrugated cardboard machines."
    
    def build(self, action_type: str, data: Dict[str, Any]) -> str:
        """
        Build a prompt by combining base instructions, specific instructions, and domain data.
        
        Args:
            action_type: The type of action ("register", "update_quantity", or "update_delivery_date").
            data: The domain data to include in the prompt.
        
        Returns:
            str: The complete prompt.
        """
        # Get the specific instructions for the action type
        specific_instruction = self.specific_instructions.get(
            action_type, 
            "Please analyze the following data and provide an optimized production plan."
        )
        
        # Combine instructions and data
        prompt = f"{self.base_instructions}\n\n{specific_instruction}\n\n"
        prompt += f"Here is the data to process:\n{json.dumps(data, default=str, indent=2)}\n\n"
        prompt += "Please provide your response as a valid JSON object with the updated production plan."
        
        return prompt