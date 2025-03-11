"""Main application module for the Moprocor backend service."""
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
import uvicorn

from config.logging import logger, log_config
from config.mongodb import init_db
from api.routes.box_router import router as box_router
from api.routes.sheet_router import router as sheet_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle.

    This context manager handles database initialization on startup.
    """
    logger.info("Initializing database connection...")
    await init_db()
    logger.info("Database initialization completed")
    yield
    logger.info("Shutting down application...")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    application = FastAPI(
        title="Moprocor API",
        description="Backend API for Moprocor service",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Root endpoint
    @application.get("/", tags=["Health"])
    async def root():
        return {"message": "Backend is up and running!"}

    # Register routers
    application.include_router(router=box_router, prefix="/boxes", tags=["Boxes"])
    application.include_router(router=sheet_router, prefix="/sheets", tags=["Sheets"])

    return application


app = create_application()

if __name__ == "__main__":
    logger.info("Starting application server...")
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_config=log_config,
            log_level=logging.INFO
        )
    except Exception as e:
        logger.error(f"Failed to start the server: {e}")