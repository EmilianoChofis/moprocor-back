from datetime import datetime, date, time
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel

class ProcessedBox(BaseModel):
    order_number: str
    symbol: str
    quantity: int
    output: int
    hierarchy: str
    part: int
    remaining: int
    arapack_lot: str

class Sheet(BaseModel):
    id: str
    ect: int
    roll_width: int
    p1: int
    p2: int
    p3: int


class ProductionRun(BaseModel):
    processed_boxes: List[ProcessedBox]
    authorized_refile: bool
    sheet: Sheet
    scheduled_date: date
    treatment: bool
    start_time: time
    end_time: time
    refile: float
    linear_meters: int
    speed: int


class ProgramPlanning(Document):
    production_runs: Optional[List[ProductionRun]] = []
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
                                "arapack_lot": "string"
                            }
                        ],
                        "authorized_refile": True,
                        "sheet": {
                            "id": "string",
                            "ect": 0,
                            "roll_width": 0,
                            "p1": 0,
                            "p2": 0,
                            "p3": 0
                        },
                        "scheduled_date": "2023-10-23",
                        "treatment": True,
                        "start_time": "2023-10-23T19:23:00",
                        "end_time": "2023-10-23T19:23:00",
                        "refile": 0,
                        "linear_meters": 0,
                        "speed": 0
                    }
                ],
                "created_at": "2023-10-23T19:23:00",
                "week_of_year": 20
            }
        }
