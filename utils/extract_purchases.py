import json
from datetime import datetime

import pandas as pd

FIELD_TYPES = {
    "receipt_date": ("datetime", None),  # Fecha de recepción
    "order_number": ("str", None),  # Número de orden
    "client": ("str", None),  # Cliente
    "symbol": ("str", None),  # Símbolo
    "repetition_new": ("str", None),  # Repetición nueva
    "type": ("str", None),  # Tipo
    "flute": ("str", None),  # Flauta
    "liner": ("str", None),  # Liner
    "ect": ("int", None),  # ECT
    "number_of_inks": ("int", None),  # Número de tintas
    "quantity": ("int", None),  # Cantidad
    "estimated_delivery_date": ("datetime", None),  # Fecha estimada de entrega
    "unit_cost": ("float", None),  # Costo unitario
    "arapack_lot": ("str", None),  # Lote Arapack
    "subtotal": ("float", None),  # Subtotal
    "total_invoice": ("float", None),  # Total de la factura
    "weight": ("float", 0.0),  # Peso
    "total_kilograms": ("float", None),  # Kilos totales
    "delivered_quantity": ("int", 0),  # Cantidad entregada
    "initial_shipping_date": ("datetime", None),  # Fecha de envío inicial
    "final_shipping_date": ("datetime", None),  # Fecha de envío final
    "delivery_dates": ("list_of_dates", []),  # Fechas de entrega
    "missing_quantity": ("int", 0),  # Cantidad faltante
    "status": ("str", None),  # Estado
    "comments": ("str", ""),  # Comentarios
    "pending_kilograms": ("float", 0.0),  # Kilos pendientes
    "delivery_delay_days": ("int", 0),  # Días de retraso en la entrega
    "real_delivery_period": ("int", 0),  # Periodo real de entrega
}

def parse_value(value, typ, default):
    """
    Convierte un valor al tipo especificado, devolviendo un valor por defecto en caso de error.

    Args:
        value: El valor a convertir.
        typ (str): El tipo al que se debe convertir el valor (str, int, float, datetime, list_of_dates).
        default: El valor por defecto a devolver si la conversión falla.

    Returns:
        El valor convertido al tipo especificado o el valor por defecto.
    """
    try:
        if pd.isna(value):
            return default
        if typ == "str":
            return str(value).strip()
        elif typ == "int":
            return int(float(value))
        elif typ == "float":
            return float(value)
        elif typ == "datetime":
            if isinstance(value, datetime):
                return value
            return pd.to_datetime(value, errors="coerce")
        elif typ == "list_of_dates":
            if isinstance(value, str):
                dates = [
                    pd.to_datetime(d.strip(), errors="coerce") for d in value.split(",")
                ]
                return [d for d in dates if pd.notna(d)]
            return []
        else:
            return value
    except Exception as e:
        print(f"Error parsing value '{value}' as {typ}: {e}")
        return default

def read_excel_to_json(excel_bytes, sheet_name):
    """
    Lee un archivo Excel y lo convierte a una lista de diccionarios en formato JSON.

    Args:
        excel_bytes: Bytes del archivo Excel.
        sheet_name (str): Nombre de la hoja a leer.

    Returns:
        list[dict]: Una lista de diccionarios con los datos formateados.

    Raises:
        ValueError: Si la hoja especificada no se encuentra o si ocurre un error al procesar el archivo.
    """
    try:
        # Find the target sheet in the Excel file
        xls = pd.ExcelFile(excel_bytes)
        available_sheets = xls.sheet_names

        target_sheet = next(
            (s for s in available_sheets if s.lower() == sheet_name.lower()), None
        )
        if not target_sheet:
            raise ValueError(
                f"La hoja '{sheet_name}' no se encuentra en el archivo Excel."
            )

        # read the target sheet into a DataFrame
        df = pd.read_excel(excel_bytes, sheet_name=target_sheet, header=None)

        # delete empty columns
        df.dropna(axis=1, how="all", inplace=True)

        # Determinate the number of rows to skip

        null_count = 0
        valid_rows = []
        for idx, row in df.iterrows():
            if row.isnull().all():
                null_count += 1
            else:
                null_count = 0
                valid_rows.append(idx)

            # If we have 3 consecutive empty rows, we stop processing
            if null_count >= 3 and len(valid_rows) > 0:
                break

        if not valid_rows:
            return []

        # Dataframe only with valid rows
        df_valid = df.iloc[valid_rows]

        field_keys = list(FIELD_TYPES.keys())

        result = []

        for _, row in df_valid.iterrows():
            purchase_data = {}

            # Mapping Excel columns to fields
            for i, value in enumerate(row):
                if i < len(field_keys):
                    field = field_keys[i]
                    field_type, default_value = FIELD_TYPES[field]
                    purchase_data[field] = parse_value(value, field_type, default_value)

            # Default values for missing fields
            for field, (field_type, default_value) in FIELD_TYPES.items():
                if field not in purchase_data:
                    purchase_data[field] = default_value

            result.append(purchase_data)

        return result

    except Exception as e:
        raise ValueError(f"Error al procesar el archivo Excel: {str(e)}")