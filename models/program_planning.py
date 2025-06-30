from datetime import datetime, date, time, timedelta
from typing import List, Optional, Annotated, Union
from beanie import Document, Link
from pydantic import BaseModel, AfterValidator


# Constants for workday schedule
WORKDAY_START = time(8, 30)  # 8:30 AM
WORKDAY_END = time(22, 0)    # 10:00 PM


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
    
    @property
    def duration(self) -> timedelta:
        return self.end_time - self.start_time
    
    @staticmethod
    async def adjust_scheduling(affected_run_id: str, operation: str = "update", target_date: Optional[date] = None):
        """Adjust scheduling for remaining runs after update/delete
        
        Args:
            affected_run_id: ID of the run being updated/deleted
            operation: Either "update" or "delete"
            target_date: Required for delete operations, the date of the deleted run
        """
        # Get the affected run to determine the date
        if operation == "update":
            affected_run = await ProductionRun.get(affected_run_id)
            target_date = affected_run.scheduled_date
        elif operation == "delete" and target_date is None:
            raise ValueError("target_date is required for delete operations")
        
        # Get all runs for the day, sorted by start_time
        runs = await ProductionRun.find(
            ProductionRun.scheduled_date == target_date
        ).sort("start_time").to_list()
        
        # Find affected run index
        if operation == "update":
            affected_index = next(
                (i for i, run in enumerate(runs) if str(run.id) == affected_run_id), -1
            )
        else:  # delete
            # For delete operations, we need to chain from the previous run's position
            affected_index = next(
                (i for i, run in enumerate(runs) if str(run.id) == affected_run_id), -1
            )
            if affected_index > -1:
                runs.pop(affected_index)  # Remove the deleted run
                affected_index -= 1  # Start chaining from previous run
        
        if affected_index == -1 and operation != "delete":
            return
        
        # Adjust runs from affected index onward
        await ProductionRun._chain_runs(runs, affected_index, WORKDAY_START, WORKDAY_END)
    
    @staticmethod
    async def _chain_runs(runs: List['ProductionRun'], start_index: int, 
                         workday_start: time, workday_end: time):
        """Chain runs maintaining continuous scheduling
        
        Args:
            runs: List of production runs to chain
            start_index: Index to start chaining from (-1 for beginning)
            workday_start: Start time of workday
            workday_end: End time of workday
        """
        if not runs:
            return
            
        # If start_index is -1, use workday start time for first run
        if start_index == -1:
            first_run = runs[0]
            first_run.start_time = datetime.combine(first_run.scheduled_date, workday_start)
            first_run.end_time = first_run.start_time + first_run.duration
            await first_run.save()
            start_index = 0
            
        for i in range(start_index + 1, len(runs)):
            prev_run = runs[i - 1]
            current_run = runs[i]
            
            # Set start_time to previous run's end_time
            current_run.start_time = prev_run.end_time
            original_duration = current_run.duration
            new_end_time = current_run.start_time + original_duration
            
            # Check if end_time exceeds workday end
            workday_end_dt = datetime.combine(current_run.scheduled_date, workday_end)
            
            if new_end_time > workday_end_dt:
                # Split the run
                remaining_duration = new_end_time - workday_end_dt
                current_run.end_time = workday_end_dt
                
                # Create overflow run for next day
                next_day = current_run.scheduled_date + timedelta(days=1)
                next_day_start = datetime.combine(next_day, workday_start)
                
                overflow_run = ProductionRun(
                    processed_boxes=current_run.processed_boxes,
                    authorized_refile=current_run.authorized_refile,
                    sheet=current_run.sheet,
                    scheduled_date=next_day,
                    treatment=current_run.treatment,
                    start_time=next_day_start,
                    end_time=next_day_start + remaining_duration,
                    refile=current_run.refile,
                    linear_meters=current_run.linear_meters,
                    speed=current_run.speed
                )
                
                await overflow_run.save()
                
                # Get next day runs and chain them
                next_day_runs = await ProductionRun.find(
                    ProductionRun.scheduled_date == next_day
                ).sort("start_time").to_list()
                
                # Insert overflow run at beginning and rechain
                next_day_runs.insert(0, overflow_run)
                await ProductionRun._chain_runs(next_day_runs, -1, workday_start, workday_end)
                
                # Stop processing current day since we've hit the end
                break
            else:
                current_run.end_time = new_end_time
                await current_run.save()

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