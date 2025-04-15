"""Box service module for interacting with the box repository."""
import os
import shutil

import dotenv
# Import the required libraries
from typing import List, Optional, Dict

from beanie import PydanticObjectId
from fastapi import HTTPException, UploadFile
from models.box import Box
from repositories.box_repository import BoxRepository

dotenv.load_dotenv()

FILES_PATH = os.getenv("FILES_PATH", "../files")

if not os.path.exists(FILES_PATH):
    os.makedirs(FILES_PATH,  exist_ok=True)


class BoxService:
    """Class for Box service."""

    @staticmethod
    async def get_all_boxes() -> List[Box]:
        """Get all boxes from the database."""
        return await BoxRepository.get_all()

    @staticmethod
    async def get_box_by_symbol(symbol: str) -> Optional[Box]:
        """Get a box by its symbol"""
        box = await BoxRepository.get_by_symbol(symbol)
        if not box:
            raise HTTPException(status_code=404, detail="Box not found")
        return await BoxRepository.get_by_symbol(symbol)

    @staticmethod
    async def create_box(box: Box, pdf_file: UploadFile) -> Box:
        """Create a box with an uploaded PDF file."""
        # Validate box data
        existing_box = await BoxRepository.get_by_symbol(box.symbol)
        if existing_box:
            raise HTTPException(
                status_code=400, detail=f"Box with symbol {box.symbol} already exists"
            )

        # Validate file type
        if not pdf_file.content_type == "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="File must be a PDF"
            )

        # If pdf_link is empty, use the original filename or create one from the symbol
        if not box.pdf_link:
            box.pdf_link = f"{box.symbol.replace(' ', '_')}.pdf"

        # Ensure the directory exists
        os.makedirs(FILES_PATH, exist_ok=True)

        # Save the PDF file
        file_path = os.path.join(FILES_PATH, box.pdf_link)

        # Create the file with proper exception handling
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(pdf_file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save PDF file: {str(e)}"
            )

        return await BoxRepository.create(box)

    @staticmethod
    async def delete_box(symbol: str) -> bool:
        """Delete a box."""
        # Implementation for deleting a box
        pass

    @staticmethod
    async def get_filtered_boxes(query: str, page: int, items_per_page: int) -> Dict[str, List[Box]]:
        """Obtiene las cajas con paginación"""

        # Calcula el offset
        offset = (page - 1) * items_per_page

        # Obtiene las cajas paginadas y el total
        return await BoxRepository.get_filtered_boxes(query, offset, items_per_page)

    @staticmethod
    async def get_pages(query: str, items_per_page: int) -> int:
        """Obtiene el total de páginas"""
        total_items = await BoxRepository.get_total_count(query)
        total_pages = (total_items + items_per_page - 1) // items_per_page  # Redondeo hacia arriba
        return total_pages

    @staticmethod
    async def get_all_symbols() -> list[str]:
        """Get all box symbols from the database."""
        return await BoxRepository.get_all_symbols()

    @staticmethod
    async def update_box(
            box_id: PydanticObjectId,
            symbol: str,
            ect: int,
            liner: str,
            width: float,
            length: float,
            flute: str,
            treatment: int,
            client: str,
            crease1: float,
            crease2: float,
            crease3: float,
            box_status: str,
            box_type: str,
            pdf_file: Optional[UploadFile]
    ) -> Optional[Box]:
        """Actualiza una caja y opcionalmente reemplaza su archivo PDF."""
        # Obtener la caja existente
        box = await BoxRepository.get_by_id(id=box_id)
        if not box:
            raise HTTPException(status_code=404, detail="Caja no encontrada")

        # Preparar los datos de actualización
        update_data = {
            "symbol": symbol,
            "ect": ect,
            "liner": liner,
            "width": width,
            "length": length,
            "flute": flute,
            "treatment": treatment,
            "client": client,
            "creases": {"r1": crease1, "r2": crease2, "r3": crease3},
            "status": box_status,
            "type": box_type,
        }

        # Manejar el reemplazo del archivo PDF
        if pdf_file:
            if not pdf_file.content_type == "application/pdf":
                raise HTTPException(
                    status_code=400,
                    detail="El archivo debe ser un PDF"
                )

            # Ruta del nuevo archivo
            new_file_path = os.path.join(FILES_PATH, pdf_file.filename)

            # Eliminar el archivo anterior si existe
            old_file_path = os.path.join(FILES_PATH, box.pdf_link)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

            # Guardar el nuevo archivo
            try:
                with open(new_file_path, "wb") as buffer:
                    shutil.copyfileobj(pdf_file.file, buffer)
                update_data["pdf_link"] = pdf_file.filename
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al guardar el archivo PDF: {str(e)}"
                )

        # Actualizar la caja en la base de datos
        updated_box = await BoxRepository.update_box(box_id, update_data)
        if not updated_box:
            raise HTTPException(status_code=404, detail="Caja no encontrada")
        return updated_box

    @staticmethod
    async def change_status(box_id: PydanticObjectId, status: str) -> Optional[Box]:
        """Change the status of a box."""
        try:
            box = await BoxRepository.change_status(box_id, status)
            if not box:
                raise HTTPException(status_code=404, detail="Box not found")
            return box
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


