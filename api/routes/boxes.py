"""
Routes for box operations using MongoDB.
"""

# Import the required libraries
from fastapi import APIRouter, HTTPException

# Import the box model
from models.box import Box

# Create a router
router = APIRouter()

# Get all boxes
@router.get("/boxes")
async def get_boxes():
    boxes = await Box.all().to_list()
    return boxes