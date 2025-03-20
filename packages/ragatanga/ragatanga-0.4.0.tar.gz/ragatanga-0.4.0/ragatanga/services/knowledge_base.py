"""
Knowledge base service implementation.

This module provides a service for knowledge base management.
"""

import os
from typing import List, Optional
from uuid import UUID

from ragatanga.repositories.knowledge_base import KnowledgeBaseRepository
from ragatanga.schemas.knowledge_base import KnowledgeBase, KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseStats


class KnowledgeBaseService:
    """
    Service for knowledge base management.
    
    Provides business logic for working with knowledge bases.
    """
    
    def __init__(self, repository: KnowledgeBaseRepository):
        """
        Initialize the service with a repository.
        
        Args:
            repository: The knowledge base repository
        """
        self.repository = repository
    
    async def create_knowledge_base(self, kb_data: KnowledgeBaseCreate) -> KnowledgeBase:
        """
        Create a new knowledge base.
        
        Args:
            kb_data: The knowledge base data
            
        Returns:
            The created knowledge base
        """
        # Validate directory path
        if hasattr(kb_data, 'directory_path') and not os.path.exists(kb_data.directory_path):
            raise ValueError(f"Knowledge base directory not found: {kb_data.directory_path}")
        
        return await self.repository.create_knowledge_base(kb_data)
    
    async def get_knowledge_base(self, kb_id: UUID) -> Optional[KnowledgeBase]:
        """
        Get a knowledge base by ID.
        
        Args:
            kb_id: The ID of the knowledge base
            
        Returns:
            The knowledge base if found, None otherwise
        """
        return await self.repository.get(kb_id)
    
    async def get_tenant_knowledge_bases(self, tenant_id: UUID) -> List[KnowledgeBase]:
        """
        Get all knowledge bases for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            
        Returns:
            A list of knowledge bases for the tenant
        """
        return await self.repository.get_tenant_knowledge_bases(tenant_id)
    
    async def get_active_knowledge_bases(self, tenant_id: UUID) -> List[KnowledgeBase]:
        """
        Get all active knowledge bases for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            
        Returns:
            A list of active knowledge bases for the tenant
        """
        return await self.repository.get_active_knowledge_bases(tenant_id)
    
    async def update_knowledge_base(self, kb_id: UUID, kb_data: KnowledgeBaseUpdate) -> Optional[KnowledgeBase]:
        """
        Update a knowledge base.
        
        Args:
            kb_id: The ID of the knowledge base to update
            kb_data: The knowledge base data
            
        Returns:
            The updated knowledge base if found, None otherwise
        """
        # Validate directory path if provided
        if hasattr(kb_data, 'directory_path') and kb_data.directory_path and not os.path.exists(kb_data.directory_path):
            raise ValueError(f"Knowledge base directory not found: {kb_data.directory_path}")
        
        return await self.repository.update_knowledge_base(kb_id, kb_data)
    
    async def delete_knowledge_base(self, kb_id: UUID) -> bool:
        """
        Delete a knowledge base.
        
        Args:
            kb_id: The ID of the knowledge base to delete
            
        Returns:
            True if the knowledge base was deleted, False otherwise
        """
        return await self.repository.delete(kb_id)
    
    async def deactivate_knowledge_base(self, kb_id: UUID) -> Optional[KnowledgeBase]:
        """
        Deactivate a knowledge base.
        
        Args:
            kb_id: The ID of the knowledge base to deactivate
            
        Returns:
            The deactivated knowledge base if found, None otherwise
        """
        return await self.repository.deactivate_knowledge_base(kb_id)
    
    async def activate_knowledge_base(self, kb_id: UUID) -> Optional[KnowledgeBase]:
        """
        Activate a knowledge base.
        
        Args:
            kb_id: The ID of the knowledge base to activate
            
        Returns:
            The activated knowledge base if found, None otherwise
        """
        return await self.repository.activate_knowledge_base(kb_id)
    
    async def get_knowledge_base_by_name(self, tenant_id: UUID, name: str) -> Optional[KnowledgeBase]:
        """
        Get a knowledge base by name for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            name: The name of the knowledge base
            
        Returns:
            The knowledge base if found, None otherwise
        """
        return await self.repository.get_knowledge_base_by_name(tenant_id, name)
    
    async def update_knowledge_base_stats(self, kb_id: UUID, stats: KnowledgeBaseStats) -> Optional[KnowledgeBase]:
        """
        Update a knowledge base's statistics.
        
        Args:
            kb_id: The ID of the knowledge base to update
            stats: The statistics to update
            
        Returns:
            The updated knowledge base if found, None otherwise
        """
        return await self.repository.update_knowledge_base_stats(kb_id, stats)
    
    async def access_knowledge_base(self, kb_id: UUID) -> Optional[KnowledgeBase]:
        """
        Record an access to a knowledge base.
        
        Args:
            kb_id: The ID of the knowledge base to update
            
        Returns:
            The updated knowledge base if found, None otherwise
        """
        return await self.repository.update_last_accessed(kb_id)
    
    async def index_knowledge_base(self, kb_id: UUID) -> Optional[KnowledgeBase]:
        """
        Index a knowledge base and update its statistics.
        
        Args:
            kb_id: The ID of the knowledge base to index
            
        Returns:
            The updated knowledge base if found, None otherwise
        """
        kb = await self.repository.get(kb_id)
        if not kb:
            return None
        
        # In a real implementation, this would scan the knowledge base directory
        # and index all documents, extracting statistics
        # For now, we'll just create some dummy statistics
        from ragatanga.config import DEFAULT_EMBEDDING_MODEL
        
        stats = KnowledgeBaseStats(
            document_count=500,
            total_tokens=1000000,
            chunk_count=5000,
            embedding_model=DEFAULT_EMBEDDING_MODEL
        )
        
        return await self.repository.update_knowledge_base_stats(kb_id, stats)
    
    async def get_knowledge_bases_by_ontology(self, ontology_id: UUID) -> List[KnowledgeBase]:
        """
        Get all knowledge bases that use a specific ontology.
        
        Args:
            ontology_id: The ID of the ontology
            
        Returns:
            A list of knowledge bases that use the ontology
        """
        if hasattr(self.repository, 'get_knowledge_bases_by_ontology'):
            return await self.repository.get_knowledge_bases_by_ontology(ontology_id)
        
        # If the repository doesn't have this method, return an empty list
        return [] 