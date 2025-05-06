from typing import List, Union

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
    machine: str



