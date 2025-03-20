"""
Tenant service implementation.

This module provides a service for tenant management.
"""

from typing import List, Optional
from uuid import UUID

from ragatanga.repositories.tenant import TenantRepository
from ragatanga.schemas.tenant import Tenant, TenantCreate, TenantUpdate


class TenantService:
    """
    Service for tenant management.
    
    Provides business logic for working with tenants.
    """
    
    def __init__(self, repository: TenantRepository):
        """
        Initialize the service with a repository.
        
        Args:
            repository: The tenant repository
        """
        self.repository = repository
    
    async def create_tenant(self, tenant_data: TenantCreate) -> Tenant:
        """
        Create a new tenant.
        
        Args:
            tenant_data: The tenant data
            
        Returns:
            The created tenant
        """
        return await self.repository.create_tenant(tenant_data)
    
    async def get_tenant(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Get a tenant by ID.
        
        Args:
            tenant_id: The ID of the tenant
            
        Returns:
            The tenant if found, None otherwise
        """
        return await self.repository.get(tenant_id)
    
    async def get_all_tenants(self) -> List[Tenant]:
        """
        Get all tenants.
        
        Returns:
            A list of all tenants
        """
        return await self.repository.get_all()
    
    async def get_active_tenants(self) -> List[Tenant]:
        """
        Get all active tenants.
        
        Returns:
            A list of active tenants
        """
        return await self.repository.get_active_tenants()
    
    async def update_tenant(self, tenant_id: UUID, tenant_data: TenantUpdate) -> Optional[Tenant]:
        """
        Update a tenant.
        
        Args:
            tenant_id: The ID of the tenant to update
            tenant_data: The tenant data
            
        Returns:
            The updated tenant if found, None otherwise
        """
        return await self.repository.update_tenant(tenant_id, tenant_data)
    
    async def delete_tenant(self, tenant_id: UUID) -> bool:
        """
        Delete a tenant.
        
        Args:
            tenant_id: The ID of the tenant to delete
            
        Returns:
            True if the tenant was deleted, False otherwise
        """
        return await self.repository.delete(tenant_id)
    
    async def deactivate_tenant(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Deactivate a tenant.
        
        Args:
            tenant_id: The ID of the tenant to deactivate
            
        Returns:
            The deactivated tenant if found, None otherwise
        """
        return await self.repository.deactivate_tenant(tenant_id)
    
    async def activate_tenant(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Activate a tenant.
        
        Args:
            tenant_id: The ID of the tenant to activate
            
        Returns:
            The activated tenant if found, None otherwise
        """
        return await self.repository.activate_tenant(tenant_id)
    
    async def get_tenant_by_name(self, name: str) -> Optional[Tenant]:
        """
        Get a tenant by name.
        
        Args:
            name: The name of the tenant
            
        Returns:
            The tenant if found, None otherwise
        """
        return await self.repository.get_tenant_by_name(name)
    
    async def update_tenant_metadata(self, tenant_id: UUID, metadata: dict) -> Optional[Tenant]:
        """
        Update a tenant's metadata.
        
        Args:
            tenant_id: The ID of the tenant to update
            metadata: The metadata to update
            
        Returns:
            The updated tenant if found, None otherwise
        """
        return await self.repository.update_tenant_metadata(tenant_id, metadata)
    
    async def increment_ontology_count(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Increment a tenant's ontology count.
        
        Args:
            tenant_id: The ID of the tenant to update
            
        Returns:
            The updated tenant if found, None otherwise
        """
        tenant = await self.repository.get(tenant_id)
        if not tenant:
            return None
        
        return await self.repository.update(tenant_id, {"ontology_count": tenant.ontology_count + 1})
    
    async def decrement_ontology_count(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Decrement a tenant's ontology count.
        
        Args:
            tenant_id: The ID of the tenant to update
            
        Returns:
            The updated tenant if found, None otherwise
        """
        tenant = await self.repository.get(tenant_id)
        if not tenant or tenant.ontology_count <= 0:
            return None
        
        return await self.repository.update(tenant_id, {"ontology_count": tenant.ontology_count - 1})
    
    async def increment_knowledge_base_count(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Increment a tenant's knowledge base count.
        
        Args:
            tenant_id: The ID of the tenant to update
            
        Returns:
            The updated tenant if found, None otherwise
        """
        tenant = await self.repository.get(tenant_id)
        if not tenant:
            return None
        
        return await self.repository.update(tenant_id, {"knowledge_base_count": tenant.knowledge_base_count + 1})
    
    async def decrement_knowledge_base_count(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Decrement a tenant's knowledge base count.
        
        Args:
            tenant_id: The ID of the tenant to update
            
        Returns:
            The updated tenant if found, None otherwise
        """
        tenant = await self.repository.get(tenant_id)
        if not tenant or tenant.knowledge_base_count <= 0:
            return None
        
        return await self.repository.update(tenant_id, {"knowledge_base_count": tenant.knowledge_base_count - 1}) 