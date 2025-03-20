"""
Knowledge base schema models.

This module defines the schema models for knowledge bases.
"""

from datetime import datetime
from typing import Dict, Optional, Any
from uuid import UUID

from pydantic import Field, field_validator

from ragatanga.schemas.base import BaseSchema
from ragatanga.config import DEFAULT_EMBEDDING_MODEL, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP


class KnowledgeBaseStats(BaseSchema):
    """
    Schema for knowledge base statistics.
    
    Provides statistical information about a knowledge base.
    """
    
    document_count: int = Field(0, description="Number of documents in the knowledge base")
    total_tokens: int = Field(0, description="Total number of tokens in the knowledge base")
    chunk_count: int = Field(0, description="Number of chunks after processing")
    embedding_model: str = Field(DEFAULT_EMBEDDING_MODEL, description="Embedding model used")


class KnowledgeBaseBase(BaseSchema):
    """
    Base schema for knowledge base data.
    
    Common attributes shared by all knowledge base schemas.
    """
    
    tenant_id: UUID = Field(description="ID of the tenant that owns this knowledge base")
    name: str = Field(description="Name of the knowledge base")
    description: Optional[str] = Field(None, description="Description of the knowledge base")
    is_active: bool = Field(True, description="Whether the knowledge base is active")
    embedding_model: str = Field(DEFAULT_EMBEDDING_MODEL, description="Embedding model used for the knowledge base")
    chunk_size: int = Field(DEFAULT_CHUNK_SIZE, description="Size of chunks when processing documents")
    chunk_overlap: int = Field(DEFAULT_CHUNK_OVERLAP, description="Overlap between chunks when processing documents")
    directory_path: str = Field(description="Path to the knowledge base directory")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the knowledge base")
    stats: Optional[KnowledgeBaseStats] = Field(None, description="Statistics about the knowledge base")
    last_accessed: Optional[datetime] = Field(None, description="When the knowledge base was last accessed")
    last_updated: Optional[datetime] = Field(None, description="When the knowledge base was last updated")
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        """Validate that the name is not empty."""
        if not v or not v.strip():
            raise ValueError("Knowledge base name must not be empty")
        return v.strip()


class KnowledgeBaseCreate(BaseSchema):
    """
    Schema for creating a new knowledge base.
    
    This schema is used for knowledge base creation requests.
    """
    
    # Required fields
    tenant_id: UUID = Field(description="ID of the tenant that owns this knowledge base")
    name: str = Field(description="Name of the knowledge base")
    directory_path: str = Field(description="Path to the knowledge base directory")
    
    # Optional fields
    description: Optional[str] = Field(None, description="Description of the knowledge base")
    is_active: bool = Field(True, description="Whether the knowledge base is active")
    embedding_model: str = Field(DEFAULT_EMBEDDING_MODEL, description="Embedding model used for the knowledge base")
    chunk_size: int = Field(DEFAULT_CHUNK_SIZE, description="Size of chunks when processing documents")
    chunk_overlap: int = Field(DEFAULT_CHUNK_OVERLAP, description="Overlap between chunks when processing documents")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the knowledge base")
    stats: Optional[KnowledgeBaseStats] = Field(None, description="Statistics about the knowledge base")


class KnowledgeBaseUpdate(BaseSchema):
    """
    Schema for updating an existing knowledge base.
    
    This schema is used for knowledge base update requests.
    """
    
    tenant_id: Optional[UUID] = Field(None, description="ID of the tenant that owns this knowledge base")
    name: Optional[str] = Field(None, description="Name of the knowledge base")
    directory_path: Optional[str] = Field(None, description="Path to the knowledge base directory")
    embedding_model: Optional[str] = Field(None, description="Embedding model used for the knowledge base")
    chunk_size: Optional[int] = Field(None, description="Size of chunks when processing documents")
    chunk_overlap: Optional[int] = Field(None, description="Overlap between chunks when processing documents")
    description: Optional[str] = Field(None, description="Description of the knowledge base")
    is_active: Optional[bool] = Field(None, description="Whether the knowledge base is active")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the knowledge base")
    
    model_config = {
        "extra": "forbid"
    }


class KnowledgeBase(KnowledgeBaseBase):
    """
    Schema for knowledge base response.
    
    This schema is used for knowledge base responses.
    """
    
    pass 