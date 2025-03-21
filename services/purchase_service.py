"""
This module contains the PurchaseService class, which is responsible for interacting with the purchase repository.
"""
from repositories.purchase_repository import PurchaseRepository


class PurchaseService:
    """ Class for Purchase service. """

    @staticmethod
    async def get_all_purchases():
        """ Get all purchases from the database. """
        return await PurchaseRepository.get_all()

    @staticmethod
    async def create_bundle(purchases):
        """ Create a new list of purchases in the database. """
        # First insert the documents
        result = await PurchaseRepository.create_bundle(purchases)

        # Then retrieve and return the newly created documents
        if result.acknowledged:
            return len(result.inserted_ids)

        return 0
