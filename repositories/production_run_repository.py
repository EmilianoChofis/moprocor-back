from models.production_run import ProductionRun

class ProductionRunRepository:
    @staticmethod
    async def get_all():
        """
        Get all production runs from the database.
        :return: List of all ProductionRun documents.
        :rtype: List[ProductionRun]
        """
        return await ProductionRun.all().to_list()

    @staticmethod
    async def create_bundle(production_runs):
        """
        Create a new list of production runs in the database.
        :param production_runs: The ProductionRun documents to create.
        :type production_runs: List[ProductionRun]
        :return: The created ProductionRun documents.
        :rtype: List[ProductionRun]
        """
        return await ProductionRun.insert_many(production_runs)