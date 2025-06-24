from datetime import datetime, date, time
from typing import List, Optional, Annotated
from beanie import Document, Link
from pydantic import BaseModel, AfterValidator


def validate_processed_boxes_length(v):
    if len(v) > 2:
        raise ValueError("A production run cannot have more than 2 processed boxes")
    return v

class SheetSnapshot(BaseModel):
    roll_width: int
    p1: int
    p2: int
    p3: int
    ect: List[int]

class ProcessedBox(BaseModel):
    order_number: str
    symbol: str
    quantity: int
    output: int
    hierarchy: str
    part: int
    remaining: int
    arapack_lot: str


class ProductionRun(Document):
    processed_boxes: Annotated[
        List[ProcessedBox], AfterValidator(validate_processed_boxes_length)
    ] = []
    authorized_refile: bool
    sheet: SheetSnapshot
    scheduled_date: date
    treatment: bool
    start_time: datetime
    end_time: datetime
    refile: float
    linear_meters: int
    speed: int

    class Settings:
        name = "production_run"

    class Config:
        json_schema_extra = {
            "example": {
                "processed_boxes": [
                    {
                        "order_number": "11109",
                        "symbol": "degasa 09",
                        "quantity": 5550,
                        "output": 2,
                        "hierarchy": "priority",
                        "part": 1,
                        "remaining": 0,
                        "arapack_lot": "0999",
                    }
                ],
                "authorized_refile": True,
                "sheet": {
                    "ect": [19,21],
                    "roll_width": 110,
                    "p1": 110,
                    "p2": 115,
                    "p3": 110,

                },
                "scheduled_date": "2025-10-23",
                "treatment": False,
                "start_time": "2025-10-23T19:23:00",
                "end_time": "2025-10-23T19:23:00",
                "refile": 5.6,
                "linear_meters": 1150,
                "speed": 70,
            }
        }


class ProgramPlanning(Document):
    production_runs: Optional[Link[ProductionRun]] = []
    created_at: datetime = datetime.now()
    week_of_year: Optional[int] = 0

    class Settings:
        name = "program_planning"

    class Config:
        json_schema_extra = {
            "example": {
                "production_runs": [
                    {
                        "processed_boxes": [
                            {
                                "order_number": "string",
                                "symbol": "string",
                                "quantity": 0,
                                "output": 0,
                                "hierarchy": "string",
                                "part": 0,
                                "remaining": 0,
                                "arapack_lot": "string",
                            }
                        ],
                        "authorized_refile": True,
                        "sheet": {
                            "id": "string",
                            "ect": 0,
                            "roll_width": 0,
                            "p1": 0,
                            "p2": 0,
                            "p3": 0,
                        },
                        "scheduled_date": "2023-10-23",
                        "treatment": True,
                        "start_time": "09:30:00",
                        "end_time": "19:23:00",
                        "refile": 0,
                        "linear_meters": 0,
                        "speed": 0,
                    }
                ],
                "created_at": "2023-10-23T19:23:00",
                "week_of_year": 20,
            }
        }
