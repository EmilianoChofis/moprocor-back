import json
from datetime import datetime
from typing import List

import pandas as pd

# Diccionario de los tipos esperados por campo
FIELD_TYPES = {
    "receipt_date": ("datetime", None),
    "order_number": ("str", None),
    "client": ("str", None),
    "symbol": ("str", None),
    "repetition_new": ("str", None),
    "type": ("str", None),
    "flute": ("str", None),
    "liner": ("str", None),
    "ect": ("int", None),
    "number_of_inks": ("int", None),
    "quantity": ("int", None),
    "estimated_delivery_date": ("datetime", None),
    "unit_cost": ("float", None),
    "arapack_lot": ("str", None),
    "subtotal": ("float", None),
    "total_invoice": ("float", None),
    "weight": ("float", 0.0),
    "total_kilograms": ("float", None),
    "delivered_quantity": ("int", 0),
    "initial_shipping_date": ("datetime", None),
    "final_shipping_date": ("datetime", None),
    "delivery_dates": ("list_of_dates", []),
    "missing_quantity": ("int", 0),
    "status": ("str", None),
    "comments": ("str", ""),
    "pending_kilograms": ("float", 0.0),
    "delivery_delay_days": ("int", 0),
    "real_delivery_period": ("int", 0),
}


def parse_value(value, typ, default):
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
            return pd.to_datetime(value, errors='coerce')
        elif typ == "list_of_dates":
            if isinstance(value, str):
                dates = [pd.to_datetime(d.strip(), errors='coerce') for d in value.split(',')]
                return [d for d in dates if pd.notna(d)]
            return []
        else:
            return value
    except Exception as e:
        print(f"Error parsing value '{value}' as {typ}: {e}")
        return default


def read_excel_to_json(file_path: str, sheet_name: str) -> List[dict]:
    # Lee el archivo para obtener los nombres de las pestañas
    all_sheets = pd.ExcelFile(file_path).sheet_names
    target_sheet = next((s for s in all_sheets if s.lower() == sheet_name.lower()), None)
    if not target_sheet:
        raise ValueError(f"Sheet '{sheet_name}' not found in Excel file.")

    df = pd.read_excel(file_path, sheet_name=target_sheet, header=None, engine='openpyxl', skiprows=2)

    # Eliminar columnas completamente vacías
    df.dropna(axis=1, how='all', inplace=True)

    # Detectar 3 filas seguidas vacías
    null_count = 0
    valid_rows = []
    for idx, row in df.iterrows():
        if row.isnull().all():
            null_count += 1
        else:
            null_count = 0
            valid_rows.append(row)
        if null_count >= 3:
            break

    if not valid_rows:
        return []

    df_valid = pd.DataFrame(valid_rows)
    df_valid.columns = list(FIELD_TYPES.keys())[:len(df_valid.columns)]  # Asignar nombres

    result = []
    for _, row in df_valid.iterrows():
        parsed_row = {}
        for col, (typ, default) in FIELD_TYPES.items():
            value = row.get(col, None)
            parsed_row[col] = parse_value(value, typ, default)
        result.append(parsed_row)

    return result


# ➤ Ejemplo de uso
if __name__ == "__main__":
    data = read_excel_to_json("CONTROL DE PEDIDOS ARAPACK 2025.xlsx", "sem 02")
    json_output = json.dumps(data, default=str, indent=2)
    print(json_output)
