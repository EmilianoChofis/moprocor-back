"""
This module defines the ProductionPlanUpdater interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ProductionPlanUpdater(ABC):
    """
    Interface for updating production plans using AI-generated responses.

    This defines a contract for each action that processes different data
    but calls the same AI pipeline.
    """

    @abstractmethod
    async def update(self, input_data: Dict[str, Any]) -> None:
        """
        Update the production plan based on the input data.

        Args:
            input_data: A dictionary containing the data needed for the update.
        """
        pass
