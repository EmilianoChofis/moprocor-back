import re

from pydantic import json

from config.aws_bedrock import AWSBedrockService
from repositories.production_run_repository import ProductionRunRepository

from typing import List, Dict, Any
from models.production_run import ProductionRun
from utils.prompt_constructor import construct_prompt


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

    @staticmethod
    async def get_plan_from_ia(purchases: List[Dict[str, Any]], sheets: List[Dict[str, any]],
                               boxes: List[Dict[str, Any]]):
        """
        Obtiene un plan de producción desde la IA utilizando AWS Bedrock.

        :param purchases: Lista de órdenes de compra
        :type purchases: List[Dict[str, Any]]
        :param sheets: Lista de láminas disponibles
        :type sheets: List[Dict[str, Any]]
        :param boxes: Lista de cajas a fabricar
        :type boxes: List[Dict[str, Any]]
        :return: El plan de producción generado por la IA
        :rtype: ProductionRun
        """
        # Construir el prompt JSON utilizando la función existente
        prompt_json = construct_prompt(purchases, sheets, boxes)
        print(prompt_json)
        # Invocar el modelo de AWS Bedrock con el prompt
        response_text = AWSBedrockService.invoke_model(prompt_json)

        # Extraer el JSON de la respuesta de texto
        try:
            # Primero intentamos parsear directamente
            try:
                response_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Si falla, intentamos extraer el JSON utilizando regex
                json_match = re.search(r'(\[|\{).*(\]|\})', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    response_data = json.loads(json_str)
                else:
                    raise ValueError("No se pudo extraer un JSON válido de la respuesta")
        except Exception as e:
            raise ValueError(f"Error al procesar la respuesta: {str(e)}\nRespuesta recibida: {response_text}")

        # Retornar los datos JSON parseados
        return response_data
