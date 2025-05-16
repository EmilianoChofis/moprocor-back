"""Define the purchase_router module"""

from typing import List
from datetime import datetime

from fastapi import HTTPException, APIRouter, status, Query, BackgroundTasks
from pydantic import BaseModel

from models.purchase import Purchase
from services.purchase_service import PurchaseService

# Create an instance of APIRouter to define the routes for the purchase module
router = APIRouter()
ITEMS_PER_PAGE = 10  # Default number of items per page for pagination

class UpdateDeliveryInfo(BaseModel):
    """Model for updating delivery information.
    attributes optionals
    """
    new_delivery_date: datetime = None
    new_quantity: int = None

@router.get("/getAll", response_model=List[Purchase])
async def get_purchases():
    """
    Retrieve all purchases.

    Returns:
        List[Purchase]: A list of all purchases.

    Raises:
        HTTPException: If an error occurs while retrieving purchases.
    """
    try:
        return await PurchaseService.get_all_purchases()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cargas las ordenes de compra : {str(e)}",
        ) from e


@router.get("/getByArapackLot", response_model=Purchase)
async def get_purchase_by_id(arapack_lot: str):
    """
    Retrieve a purchase by its Arapack lot identifier.

    Args:
        arapack_lot (str): The Arapack lot identifier of the purchase.

    Returns:
        Purchase: The purchase corresponding to the given Arapack lot.

    Raises:
        HTTPException: If the Arapack lot is empty, the purchase is not found,
                       or an error occurs while retrieving the purchase.
    """
    try:
        if not arapack_lot:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID de compra no puede estar vacío",
            )
        purchase = await PurchaseService.get_purchase_by_arapack_lot(arapack_lot)
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


@router.get("/getFilteredPurchases", response_model=List[Purchase])
async def get_filtered_purchases(
    query: str = Query("", description="Filtro de búsqueda"),
    page: int = Query(1, description="Número de página"),
):
    """
    Retrieve filtered purchases based on a search query and pagination.

    Args:
        query (str): The search filter query (default is an empty string).
        page (int): The page number for pagination (default is 1).

    Returns:
        List[Purchase]: A list of filtered purchases.

    Raises:
        HTTPException: If the page number is less than 1 or an error occurs
                       while retrieving the filtered purchases.
    """
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
            detail=f"Error al cargar las ordenes filtradas: {str(e)}",
        ) from e


@router.get("/getPages", response_model=int)
async def get_pages(query: str = Query("", description="Filtro de búsqueda")):
    """
    Retrieve the total number of pages for a given search query.

    Args:
        query (str): The search filter query (default is an empty string).

    Returns:
        int: The total number of pages.

    Raises:
        HTTPException: If an error occurs while retrieving the total pages.
    """
    try:
        return await PurchaseService.get_pages(query, ITEMS_PER_PAGE)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cargar las páginas: {str(e)}",
        ) from e


@router.post("/create", response_model=Purchase, status_code=status.HTTP_201_CREATED)
async def create_purchase(purchase: Purchase):
    """
    Create a new purchase.

    Args:
        purchase (Purchase): The purchase data to be created.

    Returns:
        Purchase: The created purchase.

    Raises:
        HTTPException: If an error occurs while creating the purchase.
    """
    try:
        return await PurchaseService.create_purchase(purchase)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create purchase: {str(e)}",
        ) from e


@router.post(
    "/create_with_ai", response_model=Purchase, status_code=status.HTTP_201_CREATED
)
async def create_purchase_with_ai(
    purchase: Purchase, background_tasks: BackgroundTasks
):
    """
    Create a new purchase and trigger AI processing in the background.

    Args:
        purchase (Purchase): The purchase data to be created.
        background_tasks (BackgroundTasks): FastAPI background tasks for asynchronous processing.

    Returns:
        Purchase: The created purchase.

    Raises:
        HTTPException: If an error occurs while creating the purchase.
    """
    try:
        return await PurchaseService.create_purchase_with_ai(purchase, background_tasks)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create purchase with AI: {str(e)}",
        ) from e


class QuantityUpdate(BaseModel):
    """Model for quantity update requests."""

    new_quantity: int


@router.put("/update_quantity/{arapack_lot}", response_model=Purchase)
async def update_purchase_quantity(
    arapack_lot: str, update_data: QuantityUpdate, background_tasks: BackgroundTasks
):
    """
    Update the quantity of a purchase and trigger AI processing in the background.

    Args:
        arapack_lot (str): The arapack lot of the purchase to update.
        update_data (QuantityUpdate): The new quantity data.
        background_tasks (BackgroundTasks): FastAPI background tasks for asynchronous processing.

    Returns:
        Purchase: The updated purchase.

    Raises:
        HTTPException: If the purchase is not found, or an error occurs during the update.
    """
    try:
        return await PurchaseService.update_purchase_quantity(
            arapack_lot, update_data.new_quantity, background_tasks
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update purchase quantity: {str(e)}",
        ) from e



@router.put("/update_delivery_date/{arapack_lot}", response_model=Purchase)
async def update_delivery_date(
    arapack_lot: str,  background_tasks: BackgroundTasks, new_delivery_date: datetime = None, new_quantity: int = None
):
    """
    Update the delivery date of a purchase and trigger AI processing in the background.

    Args:
        arapack_lot (str): The arapack lot of the purchase to update.
        new_delivery_date (datetime): The new delivery date.
        new_quantity (int): The new quantity.
        background_tasks (BackgroundTasks): FastAPI background tasks for asynchronous processing.

    Returns:
        Purchase: The updated purchase.

    Raises:
        HTTPException: If the purchase is not found, or an error occurs during the update.
    """
    try:
        return await PurchaseService.update_delivery_date(
            arapack_lot, new_delivery_date, new_quantity, background_tasks
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update delivery date: {str(e)}",
        ) from e


@router.get("/getNullDeliveryDates", response_model=List[Purchase])
async def get_null_delivery_dates():
    """
    Retrieve purchases with null delivery dates.

    Returns:
        List[Purchase]: A list of purchases with null delivery dates.

    Raises:
        HTTPException: If an error occurs while retrieving the purchases.
    """
    try:
        return await PurchaseService.get_null_delivery_dates()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve purchases with null delivery dates: {str(e)}",
        ) from e

@router.patch("/updateDeliveryInfo/{arapack_lot}", response_model=Purchase)
async def update_delivery_info(
    arapack_lot: str, update_data: UpdateDeliveryInfo
):
    """
    Update the delivery information of a purchase and trigger AI processing in the background.

    Args:
        arapack_lot (str): The arapack lot of the purchase to update.
        update_data (DeliveryDateUpdate): The new delivery date data.

    Returns:
        Purchase: The updated purchase.

    Raises:
        HTTPException: If the purchase is not found or an error occurs during the update.
    """
    try:
        return await PurchaseService.update_delivery_info(
            arapack_lot, update_data.new_delivery_date, update_data.new_quantity
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update delivery info: {str(e)}",
        ) from e
