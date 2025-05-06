from typing import List, Optional, Union

from beanie import Document
from pydantic import BaseModel
from datetime import date, time


class ProcessedBox(BaseModel):
    order_number: str
    symbol: str
    quantity: int
    output: int
    hierarchy: str
    part: int
    remaining: int
    arapack_lot: str


class AuthorizedRefile(BaseModel):
    authorized_refile: bool


class Sheet(BaseModel):
    id: str
    ect: int
    roll_width: int
    p1: int
    p2: int
    p3: int


class ProductionRun(Document):
    processed_boxes: List[Union[ProcessedBox, AuthorizedRefile]]
    sheet: Sheet
    scheduled_date: date
    treatment: int
    start_time: time
    end_time: time
    refile: float
    grams_per_m2: int
    total_weight: float
    linear_meters: int
    speed: int

    class Settings:
        name = "production_run"

    class Config:
        json_schema_extra = {
            "example": {
                "processed_boxes": [
                    {
                        "order_number": "4500247311",
                        "symbol": "DEG SUA CE-01 4017016 (PDA)",
                        "quantity": 10000,
                        "output": 3,
                        "hierarchy": "priority",
                        "part": 1,
                        "remaining": 0,
                        "arapack_lot": "25055",
                    },
                    {
                        "authorized_refile": False,
                    },
                ],
                "sheet": {
                    "id": "1",
                    "ect": 19,
                    "roll_width": 160,
                    "p1": 110,
                    "p2": 110,
                    "p3": 110,
                },
                "scheduled_date": "2025-05-08",
                "treatment": 0,
                "start_time": "08:00:00",
                "end_time": "09:00:00",
                "refile": 5.0,
                "grams_per_m2": 110,
                "total_weight": 150.56,
                "linear_meters": 2250,
                "speed": 60,
            }
        }
