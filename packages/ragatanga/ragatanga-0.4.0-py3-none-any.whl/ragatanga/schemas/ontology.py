"""
Ontology schema models for Ragatanga.

This module defines the schema models for ontology management.
"""

from datetime import datetime
from typing import Dict, Optional, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ragatanga.schemas.base import BaseSchema


class OntologyStats(BaseSchema):
    """
    Schema for ontology statistics.
    
    Provides statistical information about an ontology.
    """
    
    class_count: int = Field(0, description="Number of classes in the ontology")
    property_count: int = Field(0, description="Number of properties in the ontology")
    individual_count: int = Field(0, description="Number of individuals in the ontology")
    
    @property
    def total_elements(self) -> int:
        """Calculate the total number of elements in the ontology."""
        return self.class_count + self.property_count + self.individual_count


class OntologyMetadata(BaseModel):
    """Metadata about an ontology."""
    
    format: str = Field(..., description="Ontology format (e.g., OWL, TTL)")
    version: Optional[str] = Field(None, description="Ontology version")
    namespace: Optional[str] = Field(None, description="Primary namespace")
    source: Optional[str] = Field(None, description="Source of the ontology")
    additional_info: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "format": "TTL",
                "version": "1.2.0",
                "namespace": "http://example.org/ontology#",
                "source": "internal",
                "additional_info": {"domain": "enterprise", "author": "Knowledge Team"}
            }
        }
    }


def default_ontology_metadata() -> OntologyMetadata:
    """Create a default OntologyMetadata instance."""
    return OntologyMetadata(
        format="OWL",
        version=None,
        namespace=None,
        source=None,
        additional_info={}
    )


class OntologyBase(BaseSchema):
    """
    Base schema for ontology data.
    
    Common attributes shared by all ontology schemas.
    """
    
    tenant_id: UUID = Field(description="ID of the tenant that owns this ontology")
    name: str = Field(description="Name of the ontology")
    description: Optional[str] = Field(None, description="Description of the ontology")
    file_path: str = Field(description="Path to the ontology file")
    is_active: bool = Field(True, description="Whether the ontology is active")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the ontology")
    stats: Optional[OntologyStats] = Field(None, description="Statistics about the ontology")
    last_accessed: Optional[datetime] = Field(None, description="When the ontology was last accessed")
    
    @field_validator("name", mode="before")
    def name_must_not_be_empty(cls, v):
        """Validate that the name is not empty."""
        if not v or not v.strip():
            raise ValueError("Ontology name must not be empty")
        return v.strip()


class OntologyCreate(BaseSchema):
    """
    Schema for creating a new ontology.
    
    This schema is used for ontology creation requests.
    """
    
    # Required fields
    tenant_id: UUID = Field(description="ID of the tenant that owns this ontology")
    name: str = Field(description="Name of the ontology")
    file_path: str = Field(description="Path to the ontology file")
    
    # Optional fields
    description: Optional[str] = Field(None, description="Description of the ontology")
    is_active: bool = Field(True, description="Whether the ontology is active")
    metadata: Optional[Union[Dict[str, Any], OntologyMetadata]] = Field(None, description="Additional metadata for the ontology")
    stats: Optional[OntologyStats] = Field(None, description="Statistics about the ontology")
    last_accessed: Optional[datetime] = Field(None, description="When the ontology was last accessed")


class OntologyUpdate(BaseSchema):
    """
    Schema for updating an existing ontology.
    
    This schema is used for ontology update requests.
    """
    
    # All fields are optional for updates
    tenant_id: Optional[UUID] = Field(None, description="ID of the tenant that owns this ontology")
    name: Optional[str] = Field(None, description="Name of the ontology")
    file_path: Optional[str] = Field(None, description="Path to the ontology file")
    description: Optional[str] = Field(None, description="Description of the ontology")
    is_active: Optional[bool] = Field(None, description="Whether the ontology is active")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the ontology")
    stats: Optional[OntologyStats] = Field(None, description="Statistics about the ontology")
    last_accessed: Optional[datetime] = Field(None, description="When the ontology was last accessed")
    
    model_config = {
        "extra": "forbid"
    }


class Ontology(OntologyBase):
    """
    Schema for ontology response.
    
    This schema is used for ontology responses.
    """
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "tenant_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Enterprise Knowledge Graph",
                "description": "Enterprise-wide knowledge graph",
                "file_path": "/data/ontologies/enterprise.owl",
                "is_active": True,
                "metadata": {
                    "format": "OWL",
                    "version": "1.0.0",
                    "namespace": "http://example.org/enterprise#",
                    "source": "internal"
                },
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "last_accessed": "2023-01-03T00:00:00Z",
                "stats": {
                    "class_count": 120,
                    "property_count": 45,
                    "individual_count": 350
                }
            }
        }
    } 