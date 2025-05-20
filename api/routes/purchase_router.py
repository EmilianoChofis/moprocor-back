"""Define the purchase_router module"""

from typing import List
from datetime import datetime

from fastapi import HTTPException, APIRouter, status, Query, BackgroundTasks
from pydantic import BaseModel

from models.purchase import Purchase, DeliveryDate
from services.purchase_service import PurchaseService

# Create an instance of APIRouter to define the routes for the purchase module
router = APIRouter()
ITEMS_PER_PAGE = 15  # Default number of items per page for pagination


class UpdateDeliveryInfo(BaseModel):
    """Model for updating delivery information.
    attributes optionals
    """
    new_delivery_date: datetime = None
    new_quantity: int = None


class Backorder(BaseModel):
    """Model for backorder information."""
    arapack_lot: str
    estimated_delivery_date: datetime = None
    quantity: int = 0
    missing_quantity: int = 0
    delivery_delay_days: int = 0


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


@router.patch("/update_delivery_date/{arapack_lot}", response_model=Purchase)
async def update_delivery_date(
        arapack_lot: str, update_data: UpdateDeliveryInfo, background_tasks: BackgroundTasks
):
    """
    Update the delivery date of a purchase and trigger AI processing in the background.

    Args:
        arapack_lot (str): The arapack lot of the purchase to update.
        update_data (UpdateDeliveryInfo): The new delivery date and quantity data.
        background_tasks (BackgroundTasks): FastAPI background tasks for asynchronous processing.

    Returns:
        Purchase: The updated purchase.

    Raises:
        HTTPException: If the purchase is not found, or an error occurs during the update.
    """
    try:
        return await PurchaseService.update_delivery_date(
            arapack_lot, update_data.new_delivery_date, update_data.new_quantity, background_tasks
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


@router.patch("/createShipping/{arapack_lot}", response_model=Purchase)
async def create_shipping(arapack_lot: str, shipping: DeliveryDate):
    """
    Create a shipping entry for a purchase.

    Args:
        arapack_lot (str): The arapack lot of the purchase to update.
        shipping (Shipping): The shipping data to be created.

    Returns:
        Purchase: The updated purchase with the new shipping entry.

    Raises:
        HTTPException: If the purchase is not found or an error occurs during the update.
    """
    try:
        return await PurchaseService.create_shipping(arapack_lot, shipping.initial_shipping_date, shipping.quantity,
                                                     shipping.comment, shipping.finish_shipping_date)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create shipping: {str(e)}",
        ) from e


@router.patch("/completeShipping/{arapack_lot}", response_model=Purchase)
async def complete_shipping(arapack_lot: str, index: int):
    """
    Complete a shipping entry for a purchase.

    Args:
        arapack_lot (str): The arapack lot of the purchase to update.
        index (int): The index of the shipping entry to complete.

    Returns:
        Purchase: The updated purchase with the completed shipping entry.

    Raises:
        HTTPException: If the purchase is not found or an error occurs during the update.
    """
    try:
        print(arapack_lot, index)
        return await PurchaseService.complete_shipping(arapack_lot, index)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete shipping: {str(e)}",
        ) from e


@router.get("/getMonthlyInvoice", response_model=float)
async def get_monthly_invoice():
    """
    Retrieve the monthly invoice.

    Returns:
        str: The monthly invoice.

    Raises:
        HTTPException: If an error occurs while retrieving the invoice.
    """
    try:
        return await PurchaseService.get_monthly_invoice()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve monthly invoice: {str(e)}",
        ) from e


@router.get("/getBackorders", response_model=List[Backorder])
async def get_backorders():
    """
    Retrieve backorders.

    Returns:
        List[Purchase]: A list of backorders.

    Raises:
        HTTPException: If an error occurs while retrieving the backorders.
    """
    try:
        return await PurchaseService.get_backorders()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve backorders: {str(e)}",
        ) from e


@router.get("/getMonthlyKilograms", response_model=float)
async def get_monthly_kilograms():
    """
    Retrieve the monthly kilograms.

    Returns:
        float: The monthly kilograms.

    Raises:
        HTTPException: If an error occurs while retrieving the kilograms.
    """
    try:
        return await PurchaseService.get_monthly_kilograms()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve monthly kilograms: {str(e)}",
        ) from e


@router.patch("/changeStatus/{arapack_lot}", response_model=Purchase)
async def change_status(arapack_lot: str, new_status: str, background_tasks: BackgroundTasks):
    """
    Change the status of a purchase.

    Args:
        arapack_lot (str): The arapack lot of the purchase to update.
        new_status (str): The new status to set for the purchase.
        background_tasks (BackgroundTasks): FastAPI background tasks for asynchronous processing.

    Returns:
        Purchase: The updated purchase with the new status.

    Raises:
        HTTPException: If the purchase is not found or an error occurs during the update.
    """
    try:
        return await PurchaseService.change_status(arapack_lot, new_status, background_tasks)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change status: {str(e)}",
        ) from e
