"""
API router module.

This module defines the main API router and includes all sub-routers.
"""

from fastapi import APIRouter

from ragatanga.api.routes import tenant_router, ontology_router, knowledge_base_router

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(tenant_router, prefix="/tenants", tags=["tenants"])
api_router.include_router(ontology_router, prefix="/ontologies", tags=["ontologies"])
api_router.include_router(knowledge_base_router, prefix="/knowledge-bases", tags=["knowledge-bases"]) 