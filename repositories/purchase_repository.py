"""
Repository for Purchase documents in the database.
"""
from models.purchase import Purchase


class PurchaseRepository:
    """ Purchase repository for MongoDB using Beanie ORM functions. """

    @staticmethod
    async def get_all():
        """
        Get all purchases from the database.
        :return: List of all Purchase documents.
        :rtype: List[Purchase]
        """
        return await Purchase.all().to_list()

    @staticmethod
    async def create_bundle(purchases):
        """
        Create a new list of purchases in the database.
        :param purchases: The Purchase documents to create.
        :type purchases: Purchases
        :return: The created Purchase document.
        :rtype: Purchase
        """
        return await Purchase.insert_many(purchases)
