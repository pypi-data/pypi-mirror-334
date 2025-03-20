"""
Ontology service implementation.

This module provides a service for ontology management.
"""

import os
from typing import List, Optional
from uuid import UUID

from ragatanga.repositories.ontology import OntologyRepository
from ragatanga.schemas.ontology import Ontology, OntologyCreate, OntologyUpdate, OntologyStats


class OntologyService:
    """
    Service for ontology management.
    
    Provides business logic for working with ontologies.
    """
    
    def __init__(self, repository: OntologyRepository):
        """
        Initialize the service with a repository.
        
        Args:
            repository: The ontology repository
        """
        self.repository = repository
    
    async def create_ontology(self, ontology_data: OntologyCreate) -> Ontology:
        """
        Create a new ontology.
        
        Args:
            ontology_data: The ontology data
            
        Returns:
            The created ontology
        """
        # Validate file path
        if not os.path.exists(ontology_data.file_path):
            raise ValueError(f"Ontology file not found: {ontology_data.file_path}")
        
        return await self.repository.create_ontology(ontology_data)
    
    async def get_ontology(self, ontology_id: UUID) -> Optional[Ontology]:
        """
        Get an ontology by ID.
        
        Args:
            ontology_id: The ID of the ontology
            
        Returns:
            The ontology if found, None otherwise
        """
        return await self.repository.get(ontology_id)
    
    async def get_tenant_ontologies(self, tenant_id: UUID) -> List[Ontology]:
        """
        Get all ontologies for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            
        Returns:
            A list of ontologies for the tenant
        """
        return await self.repository.get_tenant_ontologies(tenant_id)
    
    async def get_active_ontologies(self, tenant_id: UUID) -> List[Ontology]:
        """
        Get all active ontologies for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            
        Returns:
            A list of active ontologies for the tenant
        """
        return await self.repository.get_active_ontologies(tenant_id)
    
    async def update_ontology(self, ontology_id: UUID, ontology_data: OntologyUpdate) -> Optional[Ontology]:
        """
        Update an ontology.
        
        Args:
            ontology_id: The ID of the ontology to update
            ontology_data: The ontology data
            
        Returns:
            The updated ontology if found, None otherwise
        """
        # Validate file path if provided
        if ontology_data.file_path and not os.path.exists(ontology_data.file_path):
            raise ValueError(f"Ontology file not found: {ontology_data.file_path}")
        
        return await self.repository.update_ontology(ontology_id, ontology_data)
    
    async def delete_ontology(self, ontology_id: UUID) -> bool:
        """
        Delete an ontology.
        
        Args:
            ontology_id: The ID of the ontology to delete
            
        Returns:
            True if the ontology was deleted, False otherwise
        """
        return await self.repository.delete(ontology_id)
    
    async def deactivate_ontology(self, ontology_id: UUID) -> Optional[Ontology]:
        """
        Deactivate an ontology.
        
        Args:
            ontology_id: The ID of the ontology to deactivate
            
        Returns:
            The deactivated ontology if found, None otherwise
        """
        return await self.repository.deactivate_ontology(ontology_id)
    
    async def activate_ontology(self, ontology_id: UUID) -> Optional[Ontology]:
        """
        Activate an ontology.
        
        Args:
            ontology_id: The ID of the ontology to activate
            
        Returns:
            The activated ontology if found, None otherwise
        """
        return await self.repository.activate_ontology(ontology_id)
    
    async def get_ontology_by_name(self, tenant_id: UUID, name: str) -> Optional[Ontology]:
        """
        Get an ontology by name for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            name: The name of the ontology
            
        Returns:
            The ontology if found, None otherwise
        """
        return await self.repository.get_ontology_by_name(tenant_id, name)
    
    async def update_ontology_stats(self, ontology_id: UUID, stats: OntologyStats) -> Optional[Ontology]:
        """
        Update an ontology's statistics.
        
        Args:
            ontology_id: The ID of the ontology to update
            stats: The statistics to update
            
        Returns:
            The updated ontology if found, None otherwise
        """
        return await self.repository.update_ontology_stats(ontology_id, stats)
    
    async def access_ontology(self, ontology_id: UUID) -> Optional[Ontology]:
        """
        Record an access to an ontology.
        
        Args:
            ontology_id: The ID of the ontology to update
            
        Returns:
            The updated ontology if found, None otherwise
        """
        return await self.repository.update_last_accessed(ontology_id)
    
    async def analyze_ontology(self, ontology_id: UUID) -> Optional[Ontology]:
        """
        Analyze an ontology and update its statistics.
        
        Args:
            ontology_id: The ID of the ontology to analyze
            
        Returns:
            The updated ontology if found, None otherwise
        """
        ontology = await self.repository.get(ontology_id)
        if not ontology:
            return None
        
        # In a real implementation, this would analyze the ontology file
        # and extract statistics about classes, properties, and individuals
        # For now, we'll just create some dummy statistics
        stats = OntologyStats(
            class_count=100,
            property_count=50,
            individual_count=200
        )
        
        return await self.repository.update_ontology_stats(ontology_id, stats) 