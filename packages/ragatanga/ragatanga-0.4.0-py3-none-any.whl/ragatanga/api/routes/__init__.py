"""
API routes package.

This package contains the FastAPI route definitions for the Ragatanga API.
"""

from ragatanga.api.routes.tenant import router as tenant_router
from ragatanga.api.routes.ontology import router as ontology_router
from ragatanga.api.routes.knowledge_base import router as knowledge_base_router

__all__ = [
    "tenant_router",
    "ontology_router",
    "knowledge_base_router",
] 