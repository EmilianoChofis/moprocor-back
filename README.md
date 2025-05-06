# Dynamic Prompt Constructor for AWS Bedrock

This repository contains a dynamic prompt constructor for AWS Bedrock AI models. The prompt constructor supports multiple prompt types and can be used to generate prompts for different use cases.

## Features

- Dynamic prompt construction for multiple use cases
- Support for three different prompt types:
  - Production Planning
  - Inventory Management
  - Order Optimization
- Backward compatibility with existing code
- Easy to extend with new prompt types

## Usage

### Prompt Types

The prompt constructor supports the following prompt types:

- `PRODUCTION_PLANNING`: For generating optimized combinations of boxes per sheet
- `INVENTORY_MANAGEMENT`: For analyzing inventory levels and suggesting reorder points
- `ORDER_OPTIMIZATION`: For optimizing order fulfillment

### API Endpoints

The following API endpoints are available:

- `POST /ia`: Legacy endpoint for simple text prompts
- `POST /ai/production-planning`: For production planning prompts
- `POST /ai/inventory-management`: For inventory management prompts
- `POST /ai/order-optimization`: For order optimization prompts

### Example Usage

```python
from utils.prompt_constructor import construct_prompt, PromptType

# Production Planning
data = {
    "purchases": purchases_data,
    "sheets": sheets_data,
    "boxes": boxes_data
}
prompt = construct_prompt(PromptType.PRODUCTION_PLANNING, data)

# Inventory Management
data = {
    "inventory": inventory_data,
    "demand_history": demand_history_data,
    "supplier_lead_times": supplier_lead_times_data
}
prompt = construct_prompt(PromptType.INVENTORY_MANAGEMENT, data)

# Order Optimization
data = {
    "orders": orders_data,
    "available_stock": available_stock_data,
    "production_capacity": production_capacity_data
}
prompt = construct_prompt(PromptType.ORDER_OPTIMIZATION, data)
```

## Adding New Prompt Types

To add a new prompt type:

1. Add a new enum value to the `PromptType` class in `utils/prompt_constructor.py`
2. Create a new template file in the `samples` directory
3. Update the `template_paths` dictionary in the `construct_prompt` function
4. Add a default template structure for the new prompt type
5. Create a new API endpoint in `main.py` for the new prompt type

## Testing

Run the tests with:

```bash
python -m unittest test_prompt_constructor.py
```