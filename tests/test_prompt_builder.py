"""
Tests for the PromptBuilder.
"""

import json
import pytest
from unittest.mock import patch, mock_open

from utils.prompt_builder import PromptBuilder


@pytest.fixture
def prompt_builder():
    """Create a PromptBuilder instance."""
    with patch('builtins.open', mock_open(read_data='{"base_rules": "Test base instructions"}')):
        return PromptBuilder()


def test_load_base_instructions():
    """Test loading base instructions from file."""
    # Arrange
    with patch('builtins.open', mock_open(read_data='{"base_rules": "Test base instructions"}')):
        # Act
        builder = PromptBuilder()
        
        # Assert
        assert builder.base_instructions == "Test base instructions"


def test_load_base_instructions_fallback():
    """Test fallback when loading base instructions fails."""
    # Arrange
    with patch('builtins.open', side_effect=Exception("File not found")):
        # Act
        builder = PromptBuilder()
        
        # Assert
        assert "You are an expert in optimizing production plans" in builder.base_instructions


def test_build_register_prompt(prompt_builder):
    """Test building a register prompt."""
    # Arrange
    action_type = "register"
    data = {"purchase": {"id": "123"}}
    
    # Act
    result = prompt_builder.build(action_type, data)
    
    # Assert
    assert "Test base instructions" in result
    assert "This prompt refers to a registration of a new purchase" in result
    assert json.dumps(data, indent=2) in result


def test_build_update_quantity_prompt(prompt_builder):
    """Test building an update quantity prompt."""
    # Arrange
    action_type = "update_quantity"
    data = {"purchase": {"id": "123"}}
    
    # Act
    result = prompt_builder.build(action_type, data)
    
    # Assert
    assert "Test base instructions" in result
    assert "This prompt refers to updating the quantity of an existing purchase" in result
    assert json.dumps(data, indent=2) in result


def test_build_update_delivery_date_prompt(prompt_builder):
    """Test building an update delivery date prompt."""
    # Arrange
    action_type = "update_delivery_date"
    data = {"purchase": {"id": "123"}}
    
    # Act
    result = prompt_builder.build(action_type, data)
    
    # Assert
    assert "Test base instructions" in result
    assert "This prompt refers to updating the delivery date of an existing purchase" in result
    assert json.dumps(data, indent=2) in result


def test_build_unknown_action_type(prompt_builder):
    """Test building a prompt with an unknown action type."""
    # Arrange
    action_type = "unknown"
    data = {"purchase": {"id": "123"}}
    
    # Act
    result = prompt_builder.build(action_type, data)
    
    # Assert
    assert "Test base instructions" in result
    assert "Please analyze the following data and provide an optimized production plan" in result
    assert json.dumps(data, indent=2) in result