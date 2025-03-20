"""
Query schema models for Ragatanga.

This module defines the schema models for query processing.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ragatanga.schemas.base import BaseSchema


class QueryType(str, Enum):
    """Types of queries that can be processed."""
    
    FACTUAL = "factual"
    DESCRIPTIVE = "descriptive"
    COMPARATIVE = "comparative"
    EXPLORATORY = "exploratory"
    PROCEDURAL = "procedural"
    CAUSAL = "causal"
    HYPOTHETICAL = "hypothetical"
    UNKNOWN = "unknown"


class RetrievalStrategy(str, Enum):
    """Strategies for retrieving information."""
    
    SEMANTIC_ONLY = "semantic_only"
    ONTOLOGY_ONLY = "ontology_only"
    HYBRID = "hybrid"
    AUTO = "auto"


class QueryConfig(BaseModel):
    """Configuration for a query operation."""
    
    max_results: int = Field(
        default=10, 
        ge=1, 
        le=100,
        description="Maximum number of results to return"
    )
    
    include_metadata: bool = Field(
        default=True,
        description="Whether to include metadata in results"
    )
    
    retrieval_strategy: RetrievalStrategy = Field(
        default=RetrievalStrategy.AUTO,
        description="Strategy to use for retrieving information"
    )
    
    similarity_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score for semantic search results"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "max_results": 10,
                "include_metadata": True,
                "retrieval_strategy": "hybrid",
                "similarity_threshold": 0.7
            }
        }
    }


class QuerySource(BaseModel):
    """Source of information for a query result."""
    
    type: str = Field(..., description="Type of source (e.g., 'ontology', 'document')")
    id: Optional[str] = Field(None, description="Identifier for the source")
    name: Optional[str] = Field(None, description="Name of the source")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the source")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "document",
                "id": "doc-123",
                "name": "Product Manual",
                "metadata": {"page": 42, "section": "Installation"}
            }
        }
    }


class Query(BaseSchema):
    """Schema for a query request."""
    
    tenant_id: UUID = Field(..., description="ID of the tenant making the query")
    text: str = Field(..., min_length=1, description="Query text")
    query_type: Optional[QueryType] = Field(None, description="Type of query")
    config: QueryConfig = Field(default_factory=QueryConfig, description="Query configuration")
    context: Optional[str] = Field(None, description="Additional context for the query")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "tenant_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "text": "What are the system requirements for installation?",
                "query_type": "factual",
                "config": {
                    "max_results": 5,
                    "include_metadata": True,
                    "retrieval_strategy": "hybrid",
                    "similarity_threshold": 0.7
                },
                "context": "I'm trying to install the software on a Linux server.",
                "metadata": {"user_id": "user-123", "session_id": "session-456"}
            }
        }
    }
    
    @field_validator('text')
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        """Validate that the query text is not empty."""
        v = v.strip()
        if not v:
            raise ValueError("Query text cannot be empty")
        return v


class QueryResultItem(BaseModel):
    """An individual result item from a query."""
    
    content: str = Field(..., description="Content of the result")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")
    source: QuerySource = Field(..., description="Source of the result")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "The system requires at least 4GB of RAM and 20GB of disk space.",
                "score": 0.92,
                "source": {
                    "type": "document",
                    "id": "doc-123",
                    "name": "Product Manual",
                    "metadata": {"page": 42, "section": "Installation"}
                }
            }
        }
    }


class QueryResult(BaseSchema):
    """Schema for a query result."""
    
    query_id: UUID = Field(..., description="ID of the query")
    tenant_id: UUID = Field(..., description="ID of the tenant that made the query")
    query_text: str = Field(..., description="Original query text")
    query_type: QueryType = Field(..., description="Detected query type")
    answer: str = Field(..., description="Generated answer")
    items: List[QueryResultItem] = Field(default_factory=list, description="Individual result items")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the answer")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "query_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "tenant_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "query_text": "What are the system requirements for installation?",
                "query_type": "factual",
                "answer": "The system requires at least 4GB of RAM and 20GB of disk space for installation.",
                "items": [
                    {
                        "content": "The system requires at least 4GB of RAM and 20GB of disk space.",
                        "score": 0.92,
                        "source": {
                            "type": "document",
                            "id": "doc-123",
                            "name": "Product Manual",
                            "metadata": {"page": 42, "section": "Installation"}
                        }
                    }
                ],
                "confidence": 0.85,
                "metadata": {"processing_time_ms": 120, "retrieval_strategy": "hybrid"},
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }
    } 