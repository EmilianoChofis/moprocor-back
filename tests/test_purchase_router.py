"""
Tests for the purchase router.
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from models.purchase import Purchase
from api.routes.purchase_router import router


app = FastAPI()
app.include_router(router)
client = TestClient(app)


@pytest.fixture
def sample_purchase():
    """Create a sample purchase."""
    return {
        "receipt_date": datetime.now().isoformat(),
        "order_number": "123",
        "client": "Test Client",
        "symbol": "TEST-BOX",
        "repetition_new": "REPETICION",
        "type": "CRR",
        "flute": "C",
        "liner": "KRAFT",
        "ect": 19,
        "quantity": 1000,
        "estimated_delivery_date": datetime.now().isoformat(),
        "unit_cost": 5.0,
        "arapack_lot": "12345",
        "subtotal": 5000.0,
        "total_invoice": 5800.0,
        "weight": 0.2,
        "total_kilograms": 200.0,
        "status": "ABIERTO"
    }


def test_create_purchase_with_ai(sample_purchase):
    """Test the create_with_ai endpoint."""
    # Arrange
    with patch('services.purchase_service.PurchaseService.create_purchase_with_ai', new_callable=AsyncMock) as mock_service:
        mock_service.return_value = Purchase(**sample_purchase)
        
        # Act
        response = client.post("/create_with_ai", json=sample_purchase)
        
        # Assert
        assert response.status_code == 201
        assert mock_service.called


def test_update_purchase_quantity():
    """Test the update_quantity endpoint."""
    # Arrange
    arapack_lot = "12345"
    update_data = {"new_quantity": 2000}
    
    with patch('services.purchase_service.PurchaseService.update_purchase_quantity', new_callable=AsyncMock) as mock_service:
        mock_purchase = Purchase(
            receipt_date=datetime.now(),
            order_number="123",
            client="Test Client",
            symbol="TEST-BOX",
            repetition_new="REPETICION",
            type="CRR",
            flute="C",
            liner="KRAFT",
            ect=19,
            quantity=2000,
            arapack_lot=arapack_lot,
            subtotal=5000.0,
            total_invoice=5800.0,
            total_kilograms=200.0,
            status="ABIERTO"
        )
        mock_service.return_value = mock_purchase
        
        # Act
        response = client.put(f"/update_quantity/{arapack_lot}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["quantity"] == 2000
        mock_service.assert_called_once()


def test_update_delivery_date():
    """Test the update_delivery_date endpoint."""
    # Arrange
    arapack_lot = "12345"
    new_date = datetime.now()
    update_data = {"new_delivery_date": new_date.isoformat()}
    
    with patch('services.purchase_service.PurchaseService.update_delivery_date', new_callable=AsyncMock) as mock_service:
        mock_purchase = Purchase(
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
            estimated_delivery_date=new_date,
            arapack_lot=arapack_lot,
            subtotal=5000.0,
            total_invoice=5800.0,
            total_kilograms=200.0,
            status="ABIERTO"
        )
        mock_service.return_value = mock_purchase
        
        # Act
        response = client.put(f"/update_delivery_date/{arapack_lot}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        mock_service.assert_called_once()