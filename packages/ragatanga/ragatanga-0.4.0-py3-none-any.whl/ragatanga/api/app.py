"""
FastAPI application module.

This module defines the FastAPI application and its lifecycle events.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ragatanga.api.router import api_router
from ragatanga.database.session import init_db
from ragatanga.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    API_PREFIX,
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS,
    LOG_LEVEL,
)

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        The configured FastAPI application
    """
    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_ALLOW_CREDENTIALS,
        allow_methods=CORS_ALLOW_METHODS,
        allow_headers=CORS_ALLOW_HEADERS,
    )
    
    # Include API router
    app.include_router(api_router, prefix=API_PREFIX)
    
    # Register startup and shutdown events
    register_events(app)
    
    return app


def register_events(app: FastAPI) -> None:
    """
    Register application lifecycle events.
    
    Args:
        app: The FastAPI application
    """
    
    @app.on_event("startup")
    async def startup_event():
        """
        Initialize the application on startup.
        """
        logger.info("Starting up Ragatanga API")
        await init_db()
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """
        Clean up resources on shutdown.
        """
        logger.info("Shutting down Ragatanga API")


app = create_app()
