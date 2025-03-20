"""
Retrieval configuration schemas for Ragatanga.

This module defines the configuration schemas for the retrieval system.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


class RetrievalConfig(BaseModel):
    """
    Configuration for the retrieval system.
    
    This model defines parameters for controlling the hybrid retrieval process,
    including weights for different retrieval methods and result thresholds.
    """
    # Weights for different retrieval methods
    ontology_weight: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Weight for ontology-based retrieval results"
    )
    semantic_search_weight: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Weight for semantic search results"
    )
    
    # Default confidence values
    ontology_confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Base confidence score for ontology results"
    )
    
    # Result limits
    min_results: int = Field(
        default=1,
        ge=1,
        description="Minimum number of results to return"
    )
    max_results: int = Field(
        default=10,
        ge=1,
        description="Maximum number of results to return"
    )
    max_semantic_results: int = Field(
        default=20,
        ge=1,
        description="Maximum number of semantic search results to fetch"
    )
    
    # Similarity threshold for deduplication
    similarity_threshold: float = Field(
        default=0.85,
        ge=0.0,
        le=1.0,
        description="Threshold for considering results as duplicates"
    )
    
    # Additional parameters
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional parameters for the retrieval process"
    )
    
    @field_validator('max_results')
    def max_results_must_be_greater_than_min(cls, v, values):
        """Validate that max_results is greater than or equal to min_results."""
        min_results = values.data.get('min_results', 1)
        if v < min_results:
            raise ValueError(f"max_results must be >= min_results ({min_results})")
        return v 