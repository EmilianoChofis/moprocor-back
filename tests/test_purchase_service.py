"""
Tests for the PurchaseService.
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import BackgroundTasks
from models.purchase import Purchase
from services.purchase_service import PurchaseService


@pytest.fixture
def mock_background_tasks():
    """Create a mock BackgroundTasks."""
    return MagicMock(spec=BackgroundTasks)


@pytest.fixture
def sample_purchase():
    """Create a sample purchase."""
    return Purchase(
        receipt_date=datetime.now(),
        order_number="123",
        client="Test Client",
        symbol="TEST-BOX",
        repetition_new="REPETICION",
        type="CRR",
        flute="C",
        liner="KRAFT",
        ect=19,
        quantity=1000,
        estimated_delivery_date=datetime.now(),
        unit_cost=5.0,
        arapack_lot="12345",
        subtotal=5000.0,
        total_invoice=5800.0,
        weight=0.2,
        total_kilograms=200.0,
        status="ABIERTO",
        week_of_year=1
    )


@pytest.mark.asyncio
async def test_create_purchase_with_ai(mock_background_tasks, sample_purchase):
    """Test creating a purchase with AI processing."""
    # Arrange
    with patch.object(PurchaseService, 'create_purchase', new_callable=AsyncMock) as mock_create:
        mock_create.return_value = sample_purchase
        
        # Act
        result = await PurchaseService.create_purchase_with_ai(sample_purchase, mock_background_tasks)
        
        # Assert
        mock_create.assert_called_once_with(sample_purchase)
        mock_background_tasks.add_task.assert_called_once()
        assert result == sample_purchase


@pytest.mark.asyncio
async def test_process_new_purchase_with_ai(sample_purchase):
    """Test processing a new purchase with AI."""
    # Arrange
    with patch('repositories.box_repository.BoxRepository') as mock_box_repo, \
         patch('repositories.sheet_repository.SheetRepository') as mock_sheet_repo, \
         patch.object(PurchaseService, '_register_updater') as mock_updater:
        
        mock_box = MagicMock()
        mock_box.dict.return_value = {"symbol": "TEST-BOX"}
        mock_box_repo.get_by_symbol = AsyncMock(return_value=mock_box)
        
        mock_sheet = MagicMock()
        mock_sheet.dict.return_value = {"id": "sheet1"}
        mock_sheet_repo.get_all = AsyncMock(return_value=[mock_sheet])
        
        mock_updater.update = AsyncMock()
        
        # Act
        await PurchaseService._process_new_purchase_with_ai(sample_purchase)
        
        # Assert
        mock_box_repo.get_by_symbol.assert_called_once_with(sample_purchase.symbol)
        mock_sheet_repo.get_all.assert_called_once()
        mock_updater.update.assert_called_once()
        

@pytest.mark.asyncio
async def test_update_purchase_quantity(mock_background_tasks):
    """Test updating a purchase quantity with AI processing."""
    # Arrange
    arapack_lot = "12345"
    new_quantity = 2000
    
    with patch('repositories.purchase_repository.PurchaseRepository') as mock_repo:
        mock_purchase = MagicMock(spec=Purchase)
        mock_repo.get_by_arapack_lot = AsyncMock(return_value=mock_purchase)
        
        # Act
        result = await PurchaseService.update_purchase_quantity(arapack_lot, new_quantity, mock_background_tasks)
        
        # Assert
        mock_repo.get_by_arapack_lot.assert_called_once_with(arapack_lot)
        assert mock_purchase.quantity == new_quantity
        mock_purchase.save.assert_called_once()
        mock_background_tasks.add_task.assert_called_once()
        assert result == mock_purchase


@pytest.mark.asyncio
async def test_process_quantity_update_with_ai():
    """Test processing a quantity update with AI."""
    # Arrange
    mock_purchase = MagicMock(spec=Purchase)
    mock_purchase.week_of_year = 1
    mock_purchase.dict.return_value = {"week_of_year": 1}
    
    with patch('repositories.program_planning_repository.ProgramPlanningRepository') as mock_repo, \
         patch.object(PurchaseService, '_quantity_updater') as mock_updater:
        
        mock_program = MagicMock()
        mock_program.dict.return_value = {"week_of_year": 1}
        mock_repo.get_by_week = AsyncMock(return_value=mock_program)
        
        mock_updater.update = AsyncMock()
        
        # Act
        await PurchaseService._process_quantity_update_with_ai(mock_purchase)
        
        # Assert
        mock_repo.get_by_week.assert_called_once_with(1)
        mock_updater.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_delivery_date(mock_background_tasks):
    """Test updating a delivery date with AI processing."""
    # Arrange
    arapack_lot = "12345"
    new_date = datetime.now()
    
    with patch('repositories.purchase_repository.PurchaseRepository') as mock_repo:
        mock_purchase = MagicMock(spec=Purchase)
        mock_purchase.week_of_year = 1
        mock_repo.get_by_arapack_lot = AsyncMock(return_value=mock_purchase)
        
        # Act
        result = await PurchaseService.update_delivery_date(arapack_lot, new_date, mock_background_tasks)
        
        # Assert
        mock_repo.get_by_arapack_lot.assert_called_once_with(arapack_lot)
        assert mock_purchase.estimated_delivery_date == new_date
        mock_purchase.save.assert_called_once()
        mock_background_tasks.add_task.assert_called_once()
        assert result == mock_purchase


@pytest.mark.asyncio
async def test_process_delivery_date_update_with_ai():
    """Test processing a delivery date update with AI."""
    # Arrange
    mock_purchase = MagicMock(spec=Purchase)
    mock_purchase.week_of_year = 2
    mock_purchase.dict.return_value = {"week_of_year": 2}
    original_week = 1
    
    with patch('repositories.program_planning_repository.ProgramPlanningRepository') as mock_repo, \
         patch.object(PurchaseService, '_delivery_date_updater') as mock_updater:
        
        mock_original_program = MagicMock()
        mock_original_program.dict.return_value = {"week_of_year": 1}
        
        mock_new_program = MagicMock()
        mock_new_program.dict.return_value = {"week_of_year": 2}
        
        mock_repo.get_by_week = AsyncMock(side_effect=[mock_original_program, mock_new_program])
        
        mock_updater.update = AsyncMock()
        
        # Act
        await PurchaseService._process_delivery_date_update_with_ai(mock_purchase, original_week)
        
        # Assert
        assert mock_repo.get_by_week.call_count == 2
        mock_updater.update.assert_called_once()