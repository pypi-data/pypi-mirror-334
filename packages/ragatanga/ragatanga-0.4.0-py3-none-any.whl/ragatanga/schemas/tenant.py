"""
Tenant schema models.

This module defines the schema models for tenants.
"""

from typing import Dict, Optional, Any

from pydantic import Field, field_validator

from ragatanga.schemas.base import BaseSchema


class TenantBase(BaseSchema):
    """
    Base schema for tenant data.
    
    Common attributes shared by all tenant schemas.
    """
    
    name: str = Field(description="Name of the tenant")
    description: Optional[str] = Field(None, description="Description of the tenant")
    is_active: bool = Field(True, description="Whether the tenant is active")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the tenant")
    ontology_count: int = Field(0, description="Number of ontologies owned by the tenant")
    knowledge_base_count: int = Field(0, description="Number of knowledge bases owned by the tenant")
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        """Validate that the name is not empty."""
        if not v or not v.strip():
            raise ValueError("Tenant name must not be empty")
        return v.strip()


class TenantCreate(TenantBase):
    """
    Schema for creating a new tenant.
    
    This schema is used for tenant creation requests.
    """
    
    pass


class TenantUpdate(BaseSchema):
    """
    Schema for updating an existing tenant.
    
    This schema is used for tenant update requests.
    """
    
    name: Optional[str] = Field(None, description="Name of the tenant")
    description: Optional[str] = Field(None, description="Description of the tenant")
    is_active: Optional[bool] = Field(None, description="Whether the tenant is active")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the tenant")
    
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "description": "Schema for updating an existing tenant"
        }
    }


class Tenant(TenantBase):
    """
    Schema for tenant response.
    
    This schema is used for tenant responses.
    """
    
    model_config = {
        "json_schema_extra": {
            "description": "Tenant response model with complete data",
            "examples": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Example Tenant",
                    "description": "An example tenant",
                    "is_active": True,
                    "metadata": {"industry": "technology"},
                    "ontology_count": 2,
                    "knowledge_base_count": 3,
                    "created_at": "2024-01-01T00:00:00Z"
                }
            ]
        }
    } 