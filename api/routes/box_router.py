"""
Routes for box operations using MongoDB.
"""

import json
from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Query

from models.box import Box, Crease, Ink  # Importing models for box, creases, and inks
from services.box_service import (
    BoxService,
)  # Importing service layer for box operations

# Initialize the API router for box-related endpoints
router = APIRouter()
ITEMS_PER_PAGE = 15  # Default number of items per page for pagination


@router.get("/getAll", response_model=List[Box])
async def get_boxes():
    """
    Retrieve all boxes from the database.

    Returns:
        List[Box]: A list of all boxes.
    Raises:
        HTTPException: If an error occurs while retrieving boxes.
    """
    try:
        return await BoxService.get_all_boxes()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cargar cajas: {str(e)}",
        ) from e


@router.get("/getBySymbol/{symbol}", response_model=Box)
async def get_box_by_symbol(symbol: str):
    """
    Retrieve a box by its symbol.

    Args:
        symbol (str): The symbol of the box to retrieve.

    Returns:
        Box: The box with the specified symbol.
    Raises:
        HTTPException: If the box is not found or an error occurs.
    """
    box = await BoxService.get_box_by_symbol(symbol)
    if not box:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró caja con el simbolo {symbol}",
        )
    return box


@router.post("/create", response_model=Box, status_code=status.HTTP_201_CREATED)
async def create_box(
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
    gcmi_1: str = Form(...),
    gcmi_2: str = Form(...),
    gcmi_3: str = Form(...),
    gcmi_4: str = Form(...),
    weight: float = Form(...),
    box_status: str = Form(...),
    box_type: str = Form(...),
    file: UploadFile = File(...),
):
    """
    Create a new box with the provided details.

    Args:
        symbol (str): The symbol of the box.
        ect (int): The edge crush test value.
        liner (str): The liner type.
        width (float): The width of the box.
        length (float): The length of the box.
        flute (str): The flute type.
        treatment (int): The treatment type.
        client (str): The client associated with the box.
        crease1 (float): The first crease value.
        crease2 (float): The second crease value.
        crease3 (float): The third crease value.
        gcmi_1 (str): The first ink value.
        gcmi_2 (str): The second ink value.
        gcmi_3 (str): The third ink value.
        gcmi_4 (str): The fourth ink value.
        weight (float): The weight of the box.
        box_status (str): The status of the box.
        box_type (str): The type of the box.
        file (UploadFile): The PDF file associated with the box.

    Returns:
        Box: The created box.
    Raises:
        HTTPException: If the JSON format is invalid or an error occurs.
    """
    try:
        creases = {
            "r1": crease1,
            "r2": crease2,
            "r3": crease3,
        }
        inks = {
            "gcmi_1": gcmi_1,
            "gcmi_2": gcmi_2,
            "gcmi_3": gcmi_3,
            "gcmi_4": gcmi_4,
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
            inks=Ink(**inks),
            weight=weight,
            status=box_status,
            type=box_type,
            pdf_link=file.filename,
        )
        return await BoxService.create_box(box, file)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato JSON inválido",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar la caja: {str(e)}",
        ) from e


@router.get("/getFilteredBoxes", response_model=List[Box])
async def get_filtered_boxes(
    query: str = Query("", description="Filtro de búsqueda"),
    page: int = Query(1, description="Número de página"),
):
    """
    Retrieve filtered boxes with pagination.

    Args:
        query (str): The search filter.
        page (int): The page number for pagination.

    Returns:
        List[Box]: A list of filtered boxes.
    Raises:
        HTTPException: If the page number is invalid or an error occurs.
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de página debe ser mayor a 0",
        )

    try:
        result = await BoxService.get_filtered_boxes(query, page, ITEMS_PER_PAGE)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cargar las cajas filtradas: {str(e)}",
        )


@router.get("/getPages", response_model=int)
async def get_pages(query: str = Query("", description="Filtro de búsqueda")):
    """
    Retrieve the total number of pages for filtered boxes.

    Args:
        query (str): The search filter.

    Returns:
        int: The total number of pages.
    Raises:
        HTTPException: If an error occurs while retrieving the total pages.
    """
    try:
        return await BoxService.get_pages(query, ITEMS_PER_PAGE)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cargar las páginas: {str(e)}",
        ) from e


@router.get("/getSymbols", response_model=List[str])
async def get_symbols():
    """
    Retrieve all box symbols.

    Returns:
        List[str]: A list of all box symbols.
    Raises:
        HTTPException: If an error occurs while retrieving symbols.
    """
    try:
        return await BoxService.get_all_symbols()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cargar simbolos: {str(e)}",
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
    gcmi_1: str = Form(...),
    gcmi_2: str = Form(...),
    gcmi_3: str = Form(...),
    gcmi_4: str = Form(...),
    weight: float = Form(...),
    box_status: str = Form(...),
    box_type: str = Form(...),
    pdf_file: Optional[UploadFile] = None,
):
    """
    Update a box by its ID and optionally replace its PDF file.

    Args:
        box_id (PydanticObjectId): The ID of the box to update.
        symbol (str): The updated symbol of the box.
        ect (int): The updated edge crush test value.
        liner (str): The updated liner type.
        width (float): The updated width of the box.
        length (float): The updated length of the box.
        flute (str): The updated flute type.
        treatment (int): The updated treatment type.
        client (str): The updated client associated with the box.
        crease1 (float): The updated first crease value.
        crease2 (float): The updated second crease value.
        crease3 (float): The updated third crease value.
        gcmi_1 (str): The updated first ink value.
        gcmi_2 (str): The updated second ink value.
        gcmi_3 (str): The updated third ink value.
        gcmi_4 (str): The updated fourth ink value.
        weight (float): The updated weight of the box.
        box_status (str): The updated status of the box.
        box_type (str): The updated type of the box.
        pdf_file (Optional[UploadFile]): The updated PDF file for the box.

    Returns:
        Box: The updated box.
    Raises:
        HTTPException: If an error occurs during the update.
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
            gcmi_1=gcmi_1,
            gcmi_2=gcmi_2,
            gcmi_3=gcmi_3,
            gcmi_4=gcmi_4,
            weight=weight,
            box_status=box_status,
            box_type=box_type,
            pdf_file=pdf_file,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la caja: {str(e)}",
        )


@router.patch("/changeStatus/{symbol}", response_model=Box)
async def change_status(symbol: str, box_status: str):
    """
    Change the status of a box by its ID.

    Args:
        symbol (str): The ID of the box to update.
        box_status (str): The new status of the box.

    Returns:
        Box: The updated box with the new status.
    Raises:
        HTTPException: If an error occurs during the status update.
    """
    try:
        return await BoxService.change_status(symbol, box_status)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cambiar estado de la caja: {str(e)}",
        )
