"""
Ontology repository implementation.

This module provides a repository for ontology management.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession

from ragatanga.repositories.sqlalchemy_base import SQLAlchemyRepository
from ragatanga.schemas.ontology import Ontology, OntologyCreate, OntologyUpdate, OntologyStats


class OntologyRepository(SQLAlchemyRepository[Ontology]):
    """
    Repository for ontology management.
    
    Provides CRUD operations for ontologies.
    """
    
    def __init__(self, table: Table, session: AsyncSession):
        """
        Initialize the repository with the table and session.
        
        Args:
            table: The SQLAlchemy table for ontologies
            session: The SQLAlchemy async session
        """
        super().__init__(Ontology, table, session)
    
    async def create_ontology(self, ontology_data: OntologyCreate) -> Ontology:
        """
        Create a new ontology.
        
        Args:
            ontology_data: The ontology data
            
        Returns:
            The created ontology
        """
        return await self.create(ontology_data)
    
    async def update_ontology(self, ontology_id: UUID, ontology_data: OntologyUpdate) -> Optional[Ontology]:
        """
        Update an ontology.
        
        Args:
            ontology_id: The ID of the ontology to update
            ontology_data: The ontology data
            
        Returns:
            The updated ontology if found, None otherwise
        """
        return await self.update(ontology_id, ontology_data)
    
    async def get_tenant_ontologies(self, tenant_id: UUID) -> List[Ontology]:
        """
        Get all ontologies for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            
        Returns:
            A list of ontologies for the tenant
        """
        return await self.get_all(tenant_id=tenant_id)
    
    async def get_active_ontologies(self, tenant_id: UUID) -> List[Ontology]:
        """
        Get all active ontologies for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            
        Returns:
            A list of active ontologies for the tenant
        """
        return await self.get_all(tenant_id=tenant_id, is_active=True)
    
    async def get_ontology_by_name(self, tenant_id: UUID, name: str) -> Optional[Ontology]:
        """
        Get an ontology by name for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            name: The name of the ontology
            
        Returns:
            The ontology if found, None otherwise
        """
        ontologies = await self.get_all(tenant_id=tenant_id, name=name)
        return ontologies[0] if ontologies else None
    
    async def deactivate_ontology(self, ontology_id: UUID) -> Optional[Ontology]:
        """
        Deactivate an ontology.
        
        Args:
            ontology_id: The ID of the ontology to deactivate
            
        Returns:
            The deactivated ontology if found, None otherwise
        """
        return await self.update(ontology_id, {"is_active": False})
    
    async def activate_ontology(self, ontology_id: UUID) -> Optional[Ontology]:
        """
        Activate an ontology.
        
        Args:
            ontology_id: The ID of the ontology to activate
            
        Returns:
            The activated ontology if found, None otherwise
        """
        return await self.update(ontology_id, {"is_active": True})
    
    async def update_ontology_stats(self, ontology_id: UUID, stats: OntologyStats) -> Optional[Ontology]:
        """
        Update an ontology's statistics.
        
        Args:
            ontology_id: The ID of the ontology to update
            stats: The statistics to update
            
        Returns:
            The updated ontology if found, None otherwise
        """
        return await self.update(ontology_id, {"stats": stats})
    
    async def update_last_accessed(self, ontology_id: UUID) -> Optional[Ontology]:
        """
        Update an ontology's last accessed timestamp.
        
        Args:
            ontology_id: The ID of the ontology to update
            
        Returns:
            The updated ontology if found, None otherwise
        """
        from datetime import datetime
        return await self.update(ontology_id, {"last_accessed": datetime.now()}) 