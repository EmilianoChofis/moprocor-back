import json
import os
from typing import Dict, Any


def _load_instructions() -> Dict[str, Any]:
    """
    Load the instructions from the JSON template file.

    Returns:
        Dict[str, Any]: The instructions loaded from the JSON file.
    """
    try:
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_path = os.path.join(current_dir, "templates", "instructions.json")

        with open(template_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        raise RuntimeError("Failed to load instructions from the template file.")


class PromptBuilder:
    """
    Builds prompts for AI by combining base instructions, specific instructions, and domain data.
    """

    def __init__(self):
        """Initialize the PromptBuilder."""
        self.instructions = _load_instructions()

    def build(self, action_type: str, data: Dict[str, Any]) -> str:
        """
        Build a prompt by combining base instructions, specific instructions, and domain data.

        Args:
            action_type: The type of action ("register", "update_quantity", or "update_delivery_date").
            data: The domain data to include in the prompt.

        Returns:
            str: The complete prompt.
        """
        # Get the base instructions and specific instructions for the action type
        base_instructions = self.instructions.get("instructions", "")
        specific_instruction = self.instructions.get(f"{action_type}_instructions", "")

        # Get the output format
        output_format = self.instructions.get("output_format", {})

        if action_type == "update_info":
            # Handle the specific case for update_info_instructions
            output_format = self.instructions.get("update_info_output_format", {})

        # Combine instructions, data, and output format
        prompt = f"{base_instructions}\n\n{specific_instruction}\n\n"
        prompt += f"Here is the data to process:\n{json.dumps(data, default=str, indent=2)}\n\n"
        prompt += "Please provide your response as a valid JSON object with the updated production plan.\n\n"
        prompt += f"Output format:\n{json.dumps(output_format, indent=2)}"


        return prompt
