import json
from typing import List, Dict, Any
import os


def construct_prompt(purchases: List[Dict[str, Any]], sheets: List[Dict[str, Any]], boxes: List[Dict[str, Any]]) -> str:
    """
    Construye el prompt para el modelo de IA con los datos proporcionados.

    Args:
        purchases: Lista de órdenes de compra
        sheets: Lista de láminas disponibles
        boxes: Lista de cajas a fabricar

    Returns:
        str: JSON formateado como string que contiene el prompt y los datos
    """
    # Cargar la plantilla del JSON base
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(current_dir, "samples", "prompt_json_format.json")

    with open(template_path, 'r', encoding='utf-8') as file:
        prompt_template = json.load(file)

    # Convertir las listas a formato JSON string
    purchases_json = json.dumps(purchases)
    boxes_json = json.dumps(boxes)
    sheets_json = json.dumps(sheets)

    # Reemplazar los campos en el template
    prompt_template["purchases"] = purchases_json
    prompt_template["boxes"] = boxes_json
    prompt_template["sheets"] = sheets_json

    # Retornar el JSON
    return prompt_template