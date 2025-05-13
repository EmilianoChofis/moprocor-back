"""
Tests for the ProductionPlanUpdater implementations.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from services.updaters.base_updater import ProductionPlanUpdater
from services.updaters.register_updater import RegisterUpdater
from services.updaters.quantity_updater import QuantityUpdater
from services.updaters.delivery_date_updater import DeliveryDateUpdater
from services.ia_service import IAService


@pytest.fixture
def mock_ia_service():
    """Create a mock IAService."""
    mock_service = MagicMock(spec=IAService)
    mock_service.build_prompt = MagicMock(return_value="Test prompt")
    mock_service.call = AsyncMock(return_value="Test AI response")
    mock_service.parse_response = MagicMock(return_value={"production_runs": []})
    return mock_service


@pytest.mark.asyncio
async def test_register_updater(mock_ia_service):
    """Test the RegisterUpdater."""
    # Arrange
    with patch('repositories.program_planning_repository.ProgramPlanningRepository') as mock_repo:
        mock_repo.get_by_week = AsyncMock(return_value=None)
        
        updater = RegisterUpdater(mock_ia_service)
        input_data = {
            "purchase": {"week_of_year": 1},
            "box": {},
            "sheets": []
        }
        
        # Act
        await updater.update(input_data)
        
        # Assert
        mock_ia_service.build_prompt.assert_called_once_with(
            action_type="register",
            data={
                "purchase": {"week_of_year": 1},
                "box": {},
                "sheets": []
            }
        )
        mock_ia_service.call.assert_called_once_with("Test prompt")
        mock_ia_service.parse_response.assert_called_once_with("Test AI response")


@pytest.mark.asyncio
async def test_quantity_updater(mock_ia_service):
    """Test the QuantityUpdater."""
    # Arrange
    with patch('repositories.program_planning_repository.ProgramPlanningRepository') as mock_repo:
        mock_repo.get_by_week = AsyncMock(return_value=MagicMock())
        
        updater = QuantityUpdater(mock_ia_service)
        input_data = {
            "purchase": {"week_of_year": 1},
            "program_planning": {}
        }
        
        # Act
        await updater.update(input_data)
        
        # Assert
        mock_ia_service.build_prompt.assert_called_once_with(
            action_type="update_quantity",
            data={
                "purchase": {"week_of_year": 1},
                "program_planning": {}
            }
        )
        mock_ia_service.call.assert_called_once_with("Test prompt")
        mock_ia_service.parse_response.assert_called_once_with("Test AI response")


@pytest.mark.asyncio
async def test_delivery_date_updater(mock_ia_service):
    """Test the DeliveryDateUpdater."""
    # Arrange
    with patch('repositories.program_planning_repository.ProgramPlanningRepository') as mock_repo:
        mock_repo.get_by_week = AsyncMock(return_value=MagicMock())
        
        updater = DeliveryDateUpdater(mock_ia_service)
        input_data = {
            "purchase": {"week_of_year": 2},
            "programs": {
                "original_program_planning": {"week_of_year": 1},
                "new_program_planning": {}
            }
        }
        
        # Act
        await updater.update(input_data)
        
        # Assert
        mock_ia_service.build_prompt.assert_called_once_with(
            action_type="update_delivery_date",
            data={
                "purchase": {"week_of_year": 2},
                "original_program_planning": {"week_of_year": 1},
                "new_program_planning": {}
            }
        )
        mock_ia_service.call.assert_called_once_with("Test prompt")
        mock_ia_service.parse_response.assert_called_once_with("Test AI response")