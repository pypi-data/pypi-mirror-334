"""
API package for the Ragatanga application.

This package contains the FastAPI routes and dependencies for the Ragatanga API.
"""

from ragatanga.api.router import api_router

__all__ = ["api_router"]