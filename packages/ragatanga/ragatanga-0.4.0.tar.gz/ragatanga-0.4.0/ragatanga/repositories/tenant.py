"""
Tenant repository implementation.

This module provides a repository for tenant management.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession

from ragatanga.repositories.sqlalchemy_base import SQLAlchemyRepository
from ragatanga.schemas.tenant import Tenant, TenantCreate, TenantUpdate


class TenantRepository(SQLAlchemyRepository[Tenant]):
    """
    Repository for tenant management.
    
    Provides CRUD operations for tenants.
    """
    
    def __init__(self, table: Table, session: AsyncSession):
        """
        Initialize the repository with the table and session.
        
        Args:
            table: The SQLAlchemy table for tenants
            session: The SQLAlchemy async session
        """
        super().__init__(Tenant, table, session)
    
    async def create_tenant(self, tenant_data: TenantCreate) -> Tenant:
        """
        Create a new tenant.
        
        Args:
            tenant_data: The tenant data
            
        Returns:
            The created tenant
        """
        return await self.create(tenant_data)
    
    async def update_tenant(self, tenant_id: UUID, tenant_data: TenantUpdate) -> Optional[Tenant]:
        """
        Update a tenant.
        
        Args:
            tenant_id: The ID of the tenant to update
            tenant_data: The tenant data
            
        Returns:
            The updated tenant if found, None otherwise
        """
        return await self.update(tenant_id, tenant_data)
    
    async def get_active_tenants(self) -> List[Tenant]:
        """
        Get all active tenants.
        
        Returns:
            A list of active tenants
        """
        return await self.get_all(is_active=True)
    
    async def get_tenant_by_name(self, name: str) -> Optional[Tenant]:
        """
        Get a tenant by name.
        
        Args:
            name: The name of the tenant
            
        Returns:
            The tenant if found, None otherwise
        """
        tenants = await self.get_all(name=name)
        return tenants[0] if tenants else None
    
    async def deactivate_tenant(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Deactivate a tenant.
        
        Args:
            tenant_id: The ID of the tenant to deactivate
            
        Returns:
            The deactivated tenant if found, None otherwise
        """
        return await self.update(tenant_id, {"is_active": False})
    
    async def activate_tenant(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Activate a tenant.
        
        Args:
            tenant_id: The ID of the tenant to activate
            
        Returns:
            The activated tenant if found, None otherwise
        """
        return await self.update(tenant_id, {"is_active": True})
    
    async def update_tenant_metadata(self, tenant_id: UUID, metadata: dict) -> Optional[Tenant]:
        """
        Update a tenant's metadata.
        
        Args:
            tenant_id: The ID of the tenant to update
            metadata: The metadata to update
            
        Returns:
            The updated tenant if found, None otherwise
        """
        tenant = await self.get(tenant_id)
        if not tenant:
            return None
        
        # Merge existing metadata with new metadata
        updated_metadata = {**tenant.metadata, **metadata}
        return await self.update(tenant_id, {"metadata": updated_metadata}) 