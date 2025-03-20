"""
Tenant routes module.

This module defines the API routes for tenant management.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ragatanga.schemas.tenant import Tenant, TenantCreate, TenantUpdate
from ragatanga.services.tenant import TenantService
from ragatanga.api.dependencies import get_tenant_service

router = APIRouter()


@router.post("/", response_model=Tenant, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant_data: TenantCreate,
    tenant_service: TenantService = Depends(get_tenant_service),
):
    """
    Create a new tenant.
    """
    try:
        return await tenant_service.create_tenant(tenant_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=List[Tenant])
async def get_tenants(
    active_only: bool = False,
    tenant_service: TenantService = Depends(get_tenant_service),
):
    """
    Get all tenants.
    """
    if active_only:
        return await tenant_service.get_active_tenants()
    return await tenant_service.get_all_tenants()


@router.get("/{tenant_id}", response_model=Tenant)
async def get_tenant(
    tenant_id: UUID,
    tenant_service: TenantService = Depends(get_tenant_service),
):
    """
    Get a tenant by ID.
    """
    tenant = await tenant_service.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with ID {tenant_id} not found",
        )
    return tenant


@router.put("/{tenant_id}", response_model=Tenant)
async def update_tenant(
    tenant_id: UUID,
    tenant_data: TenantUpdate,
    tenant_service: TenantService = Depends(get_tenant_service),
):
    """
    Update a tenant.
    """
    tenant = await tenant_service.update_tenant(tenant_id, tenant_data)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with ID {tenant_id} not found",
        )
    return tenant


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: UUID,
    tenant_service: TenantService = Depends(get_tenant_service),
):
    """
    Delete a tenant.
    """
    deleted = await tenant_service.delete_tenant(tenant_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with ID {tenant_id} not found",
        )


@router.post("/{tenant_id}/activate", response_model=Tenant)
async def activate_tenant(
    tenant_id: UUID,
    tenant_service: TenantService = Depends(get_tenant_service),
):
    """
    Activate a tenant.
    """
    tenant = await tenant_service.activate_tenant(tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with ID {tenant_id} not found",
        )
    return tenant


@router.post("/{tenant_id}/deactivate", response_model=Tenant)
async def deactivate_tenant(
    tenant_id: UUID,
    tenant_service: TenantService = Depends(get_tenant_service),
):
    """
    Deactivate a tenant.
    """
    tenant = await tenant_service.deactivate_tenant(tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with ID {tenant_id} not found",
        )
    return tenant


@router.get("/by-name/{name}", response_model=Optional[Tenant])
async def get_tenant_by_name(
    name: str,
    tenant_service: TenantService = Depends(get_tenant_service),
):
    """
    Get a tenant by name.
    """
    tenant = await tenant_service.get_tenant_by_name(name)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with name {name} not found",
        )
    return tenant 