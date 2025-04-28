"""Define the purchase_router module"""

import json
from typing import List

from fastapi import HTTPException, APIRouter, status, Query, Form, File, UploadFile

from models.purchase import Purchase
from services.purchase_service import PurchaseService

router = APIRouter()
ITEMS_PER_PAGE = 10


@router.get("/getAll", response_model=List[Purchase])
async def get_purchases():
    """Define the get_purchases function"""
    try:
        return await PurchaseService.get_all_purchases()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve : {str(e)}",
        ) from e


@router.get("/getByArapackLot", response_model=Purchase)
async def get_purchase_by_id(arapack_lot: str):
    try:
        if not arapack_lot:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID de compra no puede estar vacío",
            )
        purchase = await PurchaseService.get_purchase_by_arapack_lot(
            arapack_lot
        )
        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra no encontrada",
            )
        return purchase
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la compra: {str(e)}",
        ) from e


@router.post("/loadPurchasesFromExcel", status_code=status.HTTP_200_OK)
async def load_purchases_from_excel(
    file: UploadFile = File(...), sheet_name: str = Form(...)
):
    """
    Carga compras desde un archivo Excel.
    Recibe un archivo Excel y el nombre de la hoja a procesar.
    Retorna los datos formateados según el esquema definido.
    """
    try:
        # Validación básica del archivo
        if not file.filename.endswith(".xlsx"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo debe ser un Excel (.xlsx)",
            )

        # Procesar el archivo a través del servicio
        formatted_data = await PurchaseService.load_purchases(file, sheet_name)

        return {"message": "Archivo procesado correctamente", "data": formatted_data}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el archivo: {str(e)}",
        )


@router.post("/createBundle", status_code=status.HTTP_201_CREATED)
async def create_bundle(purchases: List[Purchase]):
    """Define the create_bundle function"""
    try:
        inserted_count, json_purchases, json_boxes, json_sheets = (
            await PurchaseService.create_bundle(purchases)
        )

        return {
            "message": "Purchases created successfully",
            "count": inserted_count,
            "purchases": json.loads(json_purchases) if json_purchases else {},
            "boxes": json.loads(json_boxes) if json_boxes else {},
            "sheets": json.loads(json_sheets) if json_sheets else {},
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create bundle: {str(e)}",
        ) from e


@router.get("/getFilteredPurchases", response_model=List[Purchase])
async def get_filtered_purchases(
    query: str = Query("", description="Filtro de búsqueda"),
    page: int = Query(1, description="Número de página"),
):
    """Define the get_filtered_purchases function"""
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de página debe ser mayor a 0",
        )

    try:
        result = await PurchaseService.get_filtered_purchases(
            query, page, ITEMS_PER_PAGE
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve filtered purchases: {str(e)}",
        ) from e


@router.get("/getPages", response_model=int)
async def get_pages(query: str = Query("", description="Filtro de búsqueda")):
    """Obtiene el total de páginas"""
    try:
        return await PurchaseService.get_pages(query, ITEMS_PER_PAGE)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve total pages: {str(e)}",
        ) from e


@router.post("/create", response_model=Purchase, status_code=status.HTTP_201_CREATED)
async def create_purchase(purchase: Purchase):
    """Define the create_purchase function"""
    try:
        return await PurchaseService.create_purchase(purchase)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create purchase: {str(e)}",
        ) from e
