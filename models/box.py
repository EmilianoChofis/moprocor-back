"""
Box model for MongoDB.
"""
"""
{
    "id": "03990343", //mongo ObjectID
    "symbol": "ecg-04", // no mongo ObjectID
    "ect": 19,
    "liner": "kraft",
    "width": 90,
    "length": 50,
    "flute": "c",
    "treatment": 0, // Anti-humidity treatment, 0 for NO, 1 for YES
    "client": "degasa",
    "creases": [ // Box folds
        {"r1": 8.7},
        {"r2": 18},
        {"r3": 15.2}
    ],
    "status": "approved", // approved | review | outdated
    "extra": {"type": "CRR", "machine": "flexo"}
    "pdf_link": ""
}
"""

import asyncio
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from beanie import Document, Indexed, init_beanie

class Crease(BaseModel):
    r1: Optional[float]
    r2: Optional[float]
    r3: Optional[float]

class Extra(BaseModel):
    type: str
    machine: str

class Box(Document):
    symbol: str = Indexed()
    ect: int
    liner: str
    width: int
    length: int
    flute: str
    treatment: int
    client: str
    creases: Crease
    status: str
    extra: Extra
    pdf_link: str

class Settings:
    collection = "boxes"