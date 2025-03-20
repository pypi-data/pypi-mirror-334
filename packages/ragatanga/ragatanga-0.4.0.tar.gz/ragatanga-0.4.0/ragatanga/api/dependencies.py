"""
API dependencies for Ragatanga.

This module provides FastAPI dependencies for the Ragatanga API.
"""

from typing import Optional, AsyncGenerator, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ragatanga.api.auth import get_tenant_id
from ragatanga.core.owl_retriever import UniversalOntologyManager
from ragatanga.core.semantic import SemanticSearch
from ragatanga.api.services import QueryService
from ragatanga.core.tenant import (
    tenant_ontology_manager,
    tenant_kb_manager
)
from ragatanga.database.session import get_session
from ragatanga.database.tables import tenant_table, ontology_table, knowledge_base_table
from ragatanga.repositories.tenant import TenantRepository
from ragatanga.repositories.ontology import OntologyRepository
from ragatanga.repositories.knowledge_base import KnowledgeBaseRepository
from ragatanga.services.tenant import TenantService
from ragatanga.services.ontology import OntologyService
from ragatanga.services.knowledge_base import KnowledgeBaseService


async def get_tenant_ontology_manager(tenant_id: str = Depends(get_tenant_id)) -> Optional[UniversalOntologyManager]:
    """
    Get the ontology manager for a specific tenant.
    
    Args:
        tenant_id: The tenant ID
        
    Returns:
        The tenant's ontology manager or None if not configured
    """
    return tenant_ontology_manager.get_ontology_manager(tenant_id)


async def get_tenant_semantic_search(tenant_id: str = Depends(get_tenant_id)) -> Optional[SemanticSearch]:
    """
    Get the semantic search component for a specific tenant.
    
    Args:
        tenant_id: The tenant ID
        
    Returns:
        The tenant's semantic search or None if not configured
    """
    return tenant_kb_manager.get_semantic_search(tenant_id)


async def get_query_service(
    tenant_id: str = Depends(get_tenant_id),
    ontology_manager: Optional[UniversalOntologyManager] = Depends(get_tenant_ontology_manager),
    semantic_search: Optional[SemanticSearch] = Depends(get_tenant_semantic_search)
) -> QueryService:
    """
    Get the query service for a specific tenant.
    
    Args:
        tenant_id: The tenant ID
        ontology_manager: The tenant's ontology manager
        semantic_search: The tenant's semantic search
        
    Returns:
        A configured QueryService instance
    """
    return QueryService(
        ontology_manager=ontology_manager,
        semantic_search=semantic_search
    )


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session.
    
    Yields:
        An async database session
    """
    async for session in get_session():
        yield session


async def get_tenant_repository(session: AsyncSession = Depends(get_db_session)) -> TenantRepository:
    """
    Get a tenant repository instance.
    
    Args:
        session: The database session
        
    Returns:
        A tenant repository instance
    """
    return TenantRepository(table=tenant_table, session=session)


async def get_ontology_repository(session: AsyncSession = Depends(get_db_session)) -> OntologyRepository:
    """
    Get an ontology repository instance.
    
    Args:
        session: The database session
        
    Returns:
        An ontology repository instance
    """
    return OntologyRepository(table=ontology_table, session=session)


async def get_knowledge_base_repository(session: AsyncSession = Depends(get_db_session)) -> KnowledgeBaseRepository:
    """
    Get a knowledge base repository instance.
    
    Args:
        session: The database session
        
    Returns:
        A knowledge base repository instance
    """
    return KnowledgeBaseRepository(table=knowledge_base_table, session=session)


async def get_tenant_service(
    repository: TenantRepository = Depends(get_tenant_repository),
) -> TenantService:
    """
    Get a tenant service instance.
    
    Args:
        repository: The tenant repository
        
    Returns:
        A tenant service instance
    """
    return TenantService(repository)


async def get_ontology_service(
    repository: OntologyRepository = Depends(get_ontology_repository),
) -> OntologyService:
    """
    Get an ontology service instance.
    
    Args:
        repository: The ontology repository
        
    Returns:
        An ontology service instance
    """
    return OntologyService(repository)


async def get_knowledge_base_service(
    repository: KnowledgeBaseRepository = Depends(get_knowledge_base_repository),
) -> KnowledgeBaseService:
    """
    Get a knowledge base service instance.
    
    Args:
        repository: The knowledge base repository
        
    Returns:
        A knowledge base service instance
    """
    return KnowledgeBaseService(repository)