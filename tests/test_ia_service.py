"""
Tests for the IAService.
"""

import json
import pytest
from unittest.mock import patch, MagicMock

from services.ia_service import IAService


@pytest.fixture
def ia_service():
    """Create an IAService instance."""
    return IAService()


def test_build_prompt(ia_service):
    """Test the build_prompt method."""
    # Arrange
    action_type = "register"
    data = {"purchase": {"id": "123"}}
    
    # Act
    result = ia_service.build_prompt(action_type, data)
    
    # Assert
    assert "This prompt refers to a registration of a new purchase" in result
    assert json.dumps(data, default=str, indent=2) in result


@pytest.mark.asyncio
async def test_call(ia_service):
    """Test the call method."""
    # Arrange
    prompt = "Test prompt"
    expected_response = "Test AI response"
    
    # Act
    with patch('config.aws_bedrock.AWSBedrockService.invoke_model', return_value=expected_response):
        result = await ia_service.call(prompt)
    
    # Assert
    assert result == expected_response


def test_parse_response_valid_json(ia_service):
    """Test parsing a valid JSON response."""
    # Arrange
    response = '{"production_runs": [{"id": "123"}]}'
    
    # Act
    result = ia_service.parse_response(response)
    
    # Assert
    assert result == {"production_runs": [{"id": "123"}]}


def test_parse_response_embedded_json(ia_service):
    """Test parsing a response with embedded JSON."""
    # Arrange
    response = 'Here is the result: {"production_runs": [{"id": "123"}]} Hope it helps!'
    
    # Act
    result = ia_service.parse_response(response)
    
    # Assert
    assert result == {"production_runs": [{"id": "123"}]}


def test_parse_response_invalid_json(ia_service):
    """Test parsing an invalid JSON response."""
    # Arrange
    response = 'This is not JSON'
    
    # Act
    result = ia_service.parse_response(response)
    
    # Assert
    assert result is None