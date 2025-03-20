"""
Authentication and authorization module for multi-tenant support.

This module handles tenant authentication for the Ragatanga API.
"""

from typing import Optional
from fastapi import Request, HTTPException, Header
from loguru import logger

from ragatanga.models.tenant import tenant_store


async def get_tenant_id(
    request: Request,
    x_tenant_id: Optional[str] = Header(None, description="Tenant ID for multi-tenant deployments"),
) -> str:
    """
    Extract and validate the tenant ID from request.
    
    The tenant ID can be provided in:
    1. The X-Tenant-ID header (preferred)
    2. The ?tenant_id query parameter
    3. If neither is provided, the default tenant is used
    
    Args:
        request: The FastAPI request object
        x_tenant_id: The X-Tenant-ID header value if provided
        
    Returns:
        The validated tenant ID
        
    Raises:
        HTTPException: If the tenant ID is invalid
    """
    # First check the header
    tenant_id = x_tenant_id
    
    # If not in header, check query parameters
    if not tenant_id:
        tenant_id = request.query_params.get("tenant_id")
    
    # If still not found, use the default tenant
    if not tenant_id:
        if not tenant_store.default_tenant:
            logger.error("No default tenant configured and no tenant ID provided")
            raise HTTPException(status_code=403, detail="Tenant ID required but not provided")
        tenant_id = tenant_store.default_tenant.id
        logger.debug(f"No tenant ID provided, using default tenant {tenant_id}")
    
    # Validate the tenant ID exists
    tenant = tenant_store.get_tenant(tenant_id)
    if not tenant:
        logger.warning(f"Tenant {tenant_id} not found")
        raise HTTPException(status_code=404, detail=f"Tenant {tenant_id} not found")
    
    # All checks passed
    logger.debug(f"Tenant validated: {tenant_id}")
    return tenant_id


async def get_tenant_id_optional(
    request: Request,
    x_tenant_id: Optional[str] = Header(None, description="Optional tenant ID for multi-tenant deployments"),
) -> Optional[str]:
    """
    Extract tenant ID from request, but don't require it.
    Returns None if not provided or invalid.
    
    Args:
        request: The FastAPI request object
        x_tenant_id: The X-Tenant-ID header value if provided
        
    Returns:
        The validated tenant ID or None
    """
    # First check the header
    tenant_id = x_tenant_id
    
    # If not in header, check query parameters
    if not tenant_id:
        tenant_id = request.query_params.get("tenant_id")
    
    # If still not found, return None
    if not tenant_id:
        return None
    
    # Validate the tenant ID exists
    tenant = tenant_store.get_tenant(tenant_id)
    if not tenant:
        return None
    
    # Valid tenant ID
    return tenant_id 