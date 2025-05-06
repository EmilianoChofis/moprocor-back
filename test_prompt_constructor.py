"""
Tests for the prompt constructor utility.
"""

import unittest
import json
import os
from utils.prompt_constructor import construct_prompt, PromptType, construct_production_planning_prompt


class TestPromptConstructor(unittest.TestCase):
    """Test cases for the prompt constructor utility."""

    def test_production_planning_prompt(self):
        """Test constructing a production planning prompt."""
        # Sample data
        purchases = [{"id": "p1", "customer": "Customer A", "delivery_date": "2023-06-01"}]
        sheets = [{"id": "s1", "width": 1000, "length": 2000, "ect": "A"}]
        boxes = [{"id": "b1", "width": 500, "length": 600, "height": 400, "ect": "A"}]
        
        # Construct the prompt
        prompt = construct_prompt(PromptType.PRODUCTION_PLANNING, {
            "purchases": purchases,
            "sheets": sheets,
            "boxes": boxes
        })
        
        # Verify the prompt structure
        self.assertIn("text", prompt)
        self.assertIn("purchases", prompt)
        self.assertIn("sheets", prompt)
        self.assertIn("boxes", prompt)
        
        # Verify the data was properly serialized
        self.assertIn("Customer A", prompt["purchases"])
        self.assertIn("1000", prompt["sheets"])
        self.assertIn("500", prompt["boxes"])
    
    def test_inventory_management_prompt(self):
        """Test constructing an inventory management prompt."""
        # Sample data
        inventory = [{"id": "i1", "product": "Product A", "quantity": 100}]
        demand_history = [{"product": "Product A", "month": "2023-05", "quantity": 50}]
        supplier_lead_times = [{"supplier": "Supplier X", "product": "Product A", "lead_time_days": 14}]
        
        # Construct the prompt
        prompt = construct_prompt(PromptType.INVENTORY_MANAGEMENT, {
            "inventory": inventory,
            "demand_history": demand_history,
            "supplier_lead_times": supplier_lead_times
        })
        
        # Verify the prompt structure
        self.assertIn("text", prompt)
        self.assertIn("inventory", prompt)
        self.assertIn("demand_history", prompt)
        self.assertIn("supplier_lead_times", prompt)
        
        # Verify the data was properly serialized
        self.assertIn("Product A", prompt["inventory"])
        self.assertIn("2023-05", prompt["demand_history"])
        self.assertIn("14", prompt["supplier_lead_times"])
    
    def test_order_optimization_prompt(self):
        """Test constructing an order optimization prompt."""
        # Sample data
        orders = [{"id": "o1", "customer": "Customer B", "product": "Product B", "quantity": 200}]
        available_stock = [{"product": "Product B", "quantity": 150}]
        production_capacity = {"daily_capacity": 100, "lead_time_days": 3}
        
        # Construct the prompt
        prompt = construct_prompt(PromptType.ORDER_OPTIMIZATION, {
            "orders": orders,
            "available_stock": available_stock,
            "production_capacity": production_capacity
        })
        
        # Verify the prompt structure
        self.assertIn("text", prompt)
        self.assertIn("orders", prompt)
        self.assertIn("available_stock", prompt)
        self.assertIn("production_capacity", prompt)
        
        # Verify the data was properly serialized
        self.assertIn("Customer B", prompt["orders"])
        self.assertIn("150", prompt["available_stock"])
        self.assertIn("100", prompt["production_capacity"])
    
    def test_legacy_function(self):
        """Test the legacy function for backward compatibility."""
        # Sample data
        purchases = [{"id": "p1", "customer": "Customer A", "delivery_date": "2023-06-01"}]
        sheets = [{"id": "s1", "width": 1000, "length": 2000, "ect": "A"}]
        boxes = [{"id": "b1", "width": 500, "length": 600, "height": 400, "ect": "A"}]
        
        # Construct the prompt using the legacy function
        prompt = construct_production_planning_prompt(purchases, sheets, boxes)
        
        # Verify the prompt structure
        self.assertIn("text", prompt)
        self.assertIn("purchases", prompt)
        self.assertIn("sheets", prompt)
        self.assertIn("boxes", prompt)
        
        # Verify the data was properly serialized
        self.assertIn("Customer A", prompt["purchases"])
        self.assertIn("1000", prompt["sheets"])
        self.assertIn("500", prompt["boxes"])


if __name__ == "__main__":
    unittest.main()