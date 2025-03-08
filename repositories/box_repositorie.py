"""
Box repository for MongoDB.
"""

#Imports
from models.box import Box
from typing import List, Optional

#BoxRepository class
class BoxRepository:

    #Get all boxes from the database
    @staticmethod
    async def get_all()->List[Box]:
        return await Box.all().to_list()

    #Get a box by its symbol
    @staticmethod
    async def get_by_symbol(symbol:str)->Optional[Box]:
        return await Box.find_one(Box.symbol == symbol)

    #Create a box
    @staticmethod
    async def create(box:Box)->Box:
        return await Box.insert_one(box)
