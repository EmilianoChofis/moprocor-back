from datetime import datetime
from typing import List, Optional

from beanie import Document

from models.production_run import ProductionRun


class ProgramPlanning(Document):
    corridas: Optional[List[ProductionRun]] = []
    created_at: datetime = datetime.now()
    sem: Optional[int] = 0

    class Settings:
        name = "program_planning"

    class Config:
        json_schema_extra = {
            "example": {
                "corridas": [
                    {
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
                    },
                    {
                        "processed_boxes": [
                            {
                                "order_number": "4500247311",
                                "symbol": "DEG SUA CE-01 4017016 (PDA)",
                                "quantity": 10000,
                                "output": 3,
                                "hierarchy": "priority",
                                "part": 1,
                                "remaining": 0,
                                "arapack_lot": "25056",
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
                        "scheduled_date": "2025-05-12",
                        "treatment": 0,
                        "start_time": "08:00:00",
                        "end_time": "09:00:00",
                        "refile": 5.0,
                        "grams_per_m2": 110,
                        "total_weight": 150.56,
                        "linear_meters": 2250,
                        "speed": 60,
                    },
                ],
                "created_at": "2025-05-08T00:00:00",
                "sem": 20,
            }
        }
