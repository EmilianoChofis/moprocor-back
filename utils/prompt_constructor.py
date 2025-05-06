import json
from typing import List, Dict, Any, Optional, Literal
import os
from enum import Enum


class PromptType(str, Enum):
    """Enum for the different types of prompts that can be constructed."""
    PRODUCTION_PLANNING = "production_planning"
    INVENTORY_MANAGEMENT = "inventory_management"
    ORDER_OPTIMIZATION = "order_optimization"


def construct_prompt(
    prompt_type: PromptType,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Constructs a dynamic prompt for the AI model based on the specified type and data.

    Args:
        prompt_type: The type of prompt to construct (determines which template to use)
        data: Dictionary containing the data to include in the prompt

    Returns:
        Dict[str, Any]: Formatted prompt ready to be sent to the AWS Bedrock model
    """
    # Get the template path based on the prompt type
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    template_paths = {
        PromptType.PRODUCTION_PLANNING: os.path.join(current_dir, "samples", "prompt_json_format.json"),
        PromptType.INVENTORY_MANAGEMENT: os.path.join(current_dir, "samples", "inventory_prompt_template.json"),
        PromptType.ORDER_OPTIMIZATION: os.path.join(current_dir, "samples", "order_prompt_template.json")
    }
    
    template_path = template_paths.get(prompt_type)
    
    if not template_path or not os.path.exists(template_path):
        # If template doesn't exist, use a default structure
        if prompt_type == PromptType.PRODUCTION_PLANNING:
            prompt_template = {
                "text": "You are an expert in production planning for corrugated cardboard machines. Your task is to generate optimized combinations of boxes per sheet while minimizing refile and maximizing machine efficiency.",
                "purchases": "",
                "boxes": "",
                "sheets": ""
            }
        elif prompt_type == PromptType.INVENTORY_MANAGEMENT:
            prompt_template = {
                "text": "You are an inventory management expert. Your task is to analyze the current inventory levels and suggest optimal reorder points and quantities.",
                "inventory": "",
                "demand_history": "",
                "supplier_lead_times": ""
            }
        elif prompt_type == PromptType.ORDER_OPTIMIZATION:
            prompt_template = {
                "text": "You are an order optimization expert. Your task is to analyze the current orders and suggest the most efficient way to fulfill them.",
                "orders": "",
                "available_stock": "",
                "production_capacity": ""
            }
    else:
        # Load the template from file
        with open(template_path, "r", encoding="utf-8") as file:
            prompt_template = json.load(file)
    
    # Process and insert data into the template
    for key, value in data.items():
        if key in prompt_template:
            # If the value is a list or dict, convert to JSON string
            if isinstance(value, (list, dict)):
                prompt_template[key] = json.dumps(value)
            else:
                prompt_template[key] = value
    
    return prompt_template


# For backward compatibility
def construct_production_planning_prompt(
    purchases: List[Dict[str, Any]],
    sheets: List[Dict[str, Any]],
    boxes: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Legacy function for constructing production planning prompts.
    
    Args:
        purchases: List of purchase orders
        sheets: List of available sheets
        boxes: List of boxes to manufacture
        
    Returns:
        Dict[str, Any]: Formatted prompt for production planning
    """
    data = {
        "purchases": purchases,
        "sheets": sheets,
        "boxes": boxes
    }
    return construct_prompt(PromptType.PRODUCTION_PLANNING, data)