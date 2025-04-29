from repositories.production_run_repository import ProductionRunRepository

from typing import List
from models.production_run import ProductionRun

class ProductionRunService:
    @staticmethod
    async def get_all_production_runs() -> List[ProductionRun]:
        """
        Get all production runs from the database.
        :return: List of all ProductionRun documents.
        :rtype: List[ProductionRun]
        """
        return await ProductionRunRepository.get_all()

    @staticmethod
    async def create_bundle_production_runs(production_runs):
        """
        Create a new list of production runs in the database.
        :param production_runs: The ProductionRun documents to create.
        :type production_runs: List[ProductionRun]
        :return: The created ProductionRun documents.
        :rtype: List[ProductionRun]
        """
        return await ProductionRunRepository.create_bundle(production_runs)