"""Purchase model definition."""

from typing import Optional, List
from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel


class DeliveryDate(BaseModel):
    """DeliveryDate model representing a delivery date."""

    initial_shipping_date: datetime
    quantity: int
    comment: str
    finish_shipping_date: Optional[datetime] = None


class Purchase(Document):
    """Purchase model representing a purchase document in MongoDB."""

    receipt_date: datetime
    order_number: str
    client: str
    symbol: str
    repetition_new: str
    type: str
    flute: str
    liner: str
    ect: int
    number_of_inks: Optional[int] = 0
    quantity: int
    estimated_delivery_date: Optional[datetime] = None
    unit_cost: Optional[float] = 0.0
    arapack_lot: str = Indexed(unique=True)
    subtotal: float
    total_invoice: float
    weight: Optional[float] = 0.0
    total_kilograms: float
    delivery_dates: Optional[List[DeliveryDate]] = []
    missing_quantity: Optional[int] = 0
    status: str
    comments: Optional[str] = ""
    pending_kilograms: Optional[float] = 0.0
    delivery_delay_days: Optional[int] = 0
    created_at: datetime = datetime.now()
    week_of_year: Optional[int] = None

    class Settings:
        """Settings for the Purchase model."""

        use_state_management = True
        name = "purchases"

    class Config:
        """Configuration for the Purchase model."""

        json_schema_extra = {
            "example": {
                "receipt_date": "2025-01-08T00:00:00",
                "order_number": "4500247311",
                "client": "DEGASA S.A DE C.V (PDA)",
                "symbol": "DEG SUA CE-01 4017016 (PDA)",
                "repetition_new": "REPETICION",
                "type": "CRR",
                "flute": "C",
                "liner": "KRAFT",
                "ect": 19,
                "number_of_inks": 1,
                "quantity": 10000,
                "estimated_delivery_date": "2025-01-07T00:00:00",
                "unit_cost": 6.43,
                "arapack_lot": "25055",
                "subtotal": 64300.00,
                "total_invoice": 74588.00,
                "weight": 0.222,
                "total_kilograms": 2220.00,
                "delivered_quantity": 0,
                "delivery_dates": [
                    {
                        "initial_shipping_date": "2025-01-08T00:00:00",
                        "quantity": 10000,
                        "comment": "PRUEBA",
                        "finish_shipping_date": None,
                    }
                ],
                "missing_quantity": 10000,
                "status": "ABIERTO",
                "comments": None,
                "pending_kilograms": 2220.00,
                "delivery_delay_days": -45664,
            }
        }
