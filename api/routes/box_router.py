"""
Routes for box operations using MongoDB.
"""

import json
from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Query

from models.box import Box, Crease
from services.box_service import BoxService

router = APIRouter()
ITEMS_PER_PAGE=10

@router.get("/getAll", response_model=List[Box])
async def get_boxes():
    """Define the get_boxes function"""
    try:
        return await BoxService.get_all_boxes()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve boxes: {str(e)}",
        ) from e


@router.get("/getBySymbol/{symbol}", response_model=Box)
async def get_box_by_symbol(symbol: str):
    """Define the get_box_by_symbol function"""
    box = await BoxService.get_box_by_symbol(symbol)
    if not box:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Box with symbol {symbol} not found",
        )
    return box


@router.post("/create", response_model=Box, status_code=status.HTTP_201_CREATED)
async def create_box(symbol: str = Form(...), ect: int = Form(...), liner: str = Form(...), width: float = Form(...), length: float = Form(...), flute: str = Form(...), treatment: int = Form(...), client: str = Form(...), crease1:  float = Form(...), crease2: float = Form(...), crease3: float = Form(...), box_status: str =  Form(...), box_type: str = Form(...), file: UploadFile = File(...)):
    """Define the create_box function"""
    try:
        creases = {
            "r1": crease1,
            "r2": crease2,
            "r3": crease3,
        }
        box = Box(
            symbol=symbol,
            ect=ect,
            liner=liner,
            width=width,
            length=length,
            flute=flute,
            treatment=treatment,
            client=client,
            creases=Crease(**creases),
            status=box_status,
            type=box_type,
            pdf_link=file.filename
        )
        return await BoxService.create_box(box, file)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON format for box data",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create box: {str(e)}",
        ) from e

@router.get("/getFilteredBoxes", response_model=List[Box])
async def get_filtered_boxes(
    query: str = Query("", description="Filtro de búsqueda"),
    page: int = Query(1, description="Número de página")
):
    """Obtiene las cajas con paginación"""
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de página debe ser mayor a 0"
        )

    try:
        result = await BoxService.get_filtered_boxes(query, page, ITEMS_PER_PAGE)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve boxes: {str(e)}"
        )

@router.get("/getPages", response_model=int)
async def get_pages(
        query: str = Query("", description="Filtro de búsqueda")
):
    """Obtiene el total de páginas"""
    try:
        return await BoxService.get_pages(query, ITEMS_PER_PAGE)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve total pages: {str(e)}"
        ) from e

@router.get("/getSymbols", response_model=List[str])
async def get_symbols():
    """Obtiene los símbolos de las cajas"""
    try:
        return await BoxService.get_all_symbols()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve symbols: {str(e)}"
        ) from e


@router.put("/update/{box_id}", response_model=Box)
async def update_box(
    box_id: PydanticObjectId,
    symbol: str = Form(...),
    ect: int = Form(...),
    liner: str = Form(...),
    width: float = Form(...),
    length: float = Form(...),
    flute: str = Form(...),
    treatment: int = Form(...),
    client: str = Form(...),
    crease1: float = Form(...),
    crease2: float = Form(...),
    crease3: float = Form(...),
    box_status: str = Form(...),
    box_type: str = Form(...),
    pdf_file: Optional[UploadFile] = None
):
    """
    Actualiza una caja por su ID y opcionalmente reemplaza su archivo PDF.
    """
    try:
        return await BoxService.update_box(
            box_id,
            symbol=symbol,
            ect=ect,
            liner=liner,
            width=width,
            length=length,
            flute=flute,
            treatment=treatment,
            client=client,
            crease1=crease1,
            crease2=crease2,
            crease3=crease3,
            box_status=box_status,
            box_type=box_type,
            pdf_file=pdf_file
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la caja: {str(e)}"
        )

@router.patch("/changeStatus/{box_id}", response_model=Box)
async def change_status(box_id: PydanticObjectId, box_status: str):
    """
    Change the status of a box by its ID.
    """
    try:
        return await BoxService.change_status(box_id, box_status)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change box status: {str(e)}"
        )