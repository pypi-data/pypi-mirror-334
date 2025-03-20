"""
Knowledge Base repository implementation.

This module provides a repository for knowledge base management.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession

from ragatanga.repositories.sqlalchemy_base import SQLAlchemyRepository
from ragatanga.schemas.knowledge_base import (
    KnowledgeBase,
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    KnowledgeBaseStats
)


class KnowledgeBaseRepository(SQLAlchemyRepository[KnowledgeBase]):
    """
    Repository for knowledge base management.
    
    Provides CRUD operations for knowledge bases.
    """
    
    def __init__(self, table: Table, session: AsyncSession):
        """
        Initialize the repository with the table and session.
        
        Args:
            table: The SQLAlchemy table for knowledge bases
            session: The SQLAlchemy async session
        """
        super().__init__(KnowledgeBase, table, session)
    
    async def create_knowledge_base(self, kb_data: KnowledgeBaseCreate) -> KnowledgeBase:
        """
        Create a new knowledge base.
        
        Args:
            kb_data: The knowledge base data
            
        Returns:
            The created knowledge base
        """
        return await self.create(kb_data)
    
    async def update_knowledge_base(self, kb_id: UUID, kb_data: KnowledgeBaseUpdate) -> Optional[KnowledgeBase]:
        """
        Update a knowledge base.
        
        Args:
            kb_id: The ID of the knowledge base to update
            kb_data: The knowledge base data
            
        Returns:
            The updated knowledge base if found, None otherwise
        """
        return await self.update(kb_id, kb_data)
    
    async def get_tenant_knowledge_bases(self, tenant_id: UUID) -> List[KnowledgeBase]:
        """
        Get all knowledge bases for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            
        Returns:
            A list of knowledge bases for the tenant
        """
        return await self.get_all(tenant_id=tenant_id)
    
    async def get_active_knowledge_bases(self, tenant_id: UUID) -> List[KnowledgeBase]:
        """
        Get all active knowledge bases for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            
        Returns:
            A list of active knowledge bases for the tenant
        """
        return await self.get_all(tenant_id=tenant_id, is_active=True)
    
    async def get_knowledge_base_by_name(self, tenant_id: UUID, name: str) -> Optional[KnowledgeBase]:
        """
        Get a knowledge base by name for a tenant.
        
        Args:
            tenant_id: The ID of the tenant
            name: The name of the knowledge base
            
        Returns:
            The knowledge base if found, None otherwise
        """
        kbs = await self.get_all(tenant_id=tenant_id, name=name)
        return kbs[0] if kbs else None
    
    async def deactivate_knowledge_base(self, kb_id: UUID) -> Optional[KnowledgeBase]:
        """
        Deactivate a knowledge base.
        
        Args:
            kb_id: The ID of the knowledge base to deactivate
            
        Returns:
            The deactivated knowledge base if found, None otherwise
        """
        return await self.update(kb_id, {"is_active": False})
    
    async def activate_knowledge_base(self, kb_id: UUID) -> Optional[KnowledgeBase]:
        """
        Activate a knowledge base.
        
        Args:
            kb_id: The ID of the knowledge base to activate
            
        Returns:
            The activated knowledge base if found, None otherwise
        """
        return await self.update(kb_id, {"is_active": True})
    
    async def update_knowledge_base_stats(self, kb_id: UUID, stats: KnowledgeBaseStats) -> Optional[KnowledgeBase]:
        """
        Update a knowledge base's statistics.
        
        Args:
            kb_id: The ID of the knowledge base to update
            stats: The statistics to update
            
        Returns:
            The updated knowledge base if found, None otherwise
        """
        return await self.update(kb_id, {"stats": stats})
    
    async def update_last_accessed(self, kb_id: UUID) -> Optional[KnowledgeBase]:
        """
        Update a knowledge base's last accessed timestamp.
        
        Args:
            kb_id: The ID of the knowledge base to update
            
        Returns:
            The updated knowledge base if found, None otherwise
        """
        from datetime import datetime
        return await self.update(kb_id, {"last_accessed": datetime.now()})
    
    async def update_last_updated(self, kb_id: UUID) -> Optional[KnowledgeBase]:
        """
        Update a knowledge base's last updated timestamp.
        
        Args:
            kb_id: The ID of the knowledge base to update
            
        Returns:
            The updated knowledge base if found, None otherwise
        """
        from datetime import datetime
        return await self.update(kb_id, {"last_updated": datetime.now()})
    
    async def get_by_embedding_model(self, tenant_id: UUID, embedding_model: str) -> List[KnowledgeBase]:
        """
        Get all knowledge bases for a tenant with a specific embedding model.
        
        Args:
            tenant_id: The ID of the tenant
            embedding_model: The embedding model to filter by
            
        Returns:
            A list of knowledge bases with the specified embedding model
        """
        return await self.get_all(tenant_id=tenant_id, embedding_model=embedding_model) 