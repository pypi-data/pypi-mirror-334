"""
Pydantic models for API requests and responses.
"""

from typing import List, Dict, Any, Optional, Callable
from pydantic import BaseModel, Field

# Re-export shared models from core to maintain compatibility
from ragatanga.core.models import QueryResponse, RetrievedData, EntityInfo

__all__ = ["QueryRequest", "StatusResponse", "OntologyStatistics", 
           "TenantCreateRequest", "TenantResponse", "TenantUpdateRequest", 
           "TenantListResponse", "QueryResponse", "RetrievedData", "EntityInfo"]

class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    query: str = Field(..., description="The query string")

# Use the inherited RetrievedData, EntityInfo, and QueryResponse classes from core.models module

class StatusResponse(BaseModel):
    """Response model for status messages."""
    message: str = Field(..., description="Status message")
    success: bool = Field(True, description="Whether the operation was successful")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")

class OntologyStatistics(BaseModel):
    """Model for ontology statistics."""
    statistics: Dict[str, int] = Field(..., description="Overall statistics")
    classes: Dict[str, Dict[str, Any]] = Field(..., description="Class information")
    properties: Dict[str, Dict[str, Any]] = Field(..., description="Property information")
    individuals: Dict[str, Dict[str, Any]] = Field(..., description="Individual information")
    metadata: Dict[str, Any] = Field(..., description="Metadata about the ontology")

class TenantCreateRequest(BaseModel):
    """Request model for tenant creation."""
    name: str = Field(..., description="The name of the tenant")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=lambda: dict(), description="Optional metadata for the tenant")

class TenantResponse(BaseModel):
    """Response model for tenant operations."""
    id: str = Field(..., description="Unique identifier for the tenant")
    name: str = Field(..., description="The name of the tenant")
    created_at: str = Field(..., description="Timestamp when the tenant was created")
    updated_at: str = Field(..., description="Timestamp when the tenant was last updated")
    metadata: Dict[str, Any] = Field(default_factory=lambda: dict(), description="Tenant metadata")

class TenantUpdateRequest(BaseModel):
    """Request model for tenant updates."""
    name: Optional[str] = Field(None, description="The new name for the tenant")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Updated metadata for the tenant")

class TenantListResponse(BaseModel):
    """Response model for listing tenants."""
    tenants: List[TenantResponse] = Field(..., description="List of tenants")