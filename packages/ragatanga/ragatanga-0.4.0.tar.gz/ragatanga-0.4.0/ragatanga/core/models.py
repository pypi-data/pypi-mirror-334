"""
Shared data models for Ragatanga core components.

This module contains models shared between different parts of the system
to prevent circular imports.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RetrievalResult(BaseModel):
    """
    Model for a single retrieval result.
    
    This represents a single piece of information retrieved from
    any source (ontology or semantic search).
    """
    content: str = Field(..., description="The content of the retrieval result")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata about the result (source, query, etc.)"
    )
    confidence: float = Field(
        default=1.0,
        description="Confidence score for this result (0.0 to 1.0)"
    )


class RetrievedData(BaseModel):
    """
    Model for retrieved data from different sources.
    
    This model organizes retrieval results by their source 
    (semantic search or SPARQL query) to provide clear context
    about where information came from.
    """
    sparql: List[str] = Field(
        default_factory=list, 
        description="Results retrieved from SPARQL queries"
    )
    semantic: List[str] = Field(
        default_factory=list, 
        description="Results retrieved from semantic search"
    )
    
    @property
    def combined(self) -> List[str]:
        """Get combined results from all sources."""
        return self.sparql + self.semantic


class EntityInfo(BaseModel):
    """
    Model for entity information extracted from results.
    
    This represents structured information about entities found
    in the retrieval results, including counts and categorized lists.
    """
    counts: Dict[str, int] = Field(
        default_factory=dict, 
        description="Counts of entities by type"
    )
    lists: Dict[str, List[str]] = Field(
        default_factory=dict, 
        description="Lists of entities by type"
    )


class QueryResponse(BaseModel):
    """
    Response model for query processing.
    
    This model represents the complete response to a user query,
    including the generated answer and supporting information.
    """
    # Retrieved information
    retrieval: RetrievedData = Field(
        default_factory=RetrievedData,
        description="Data retrieved from different sources that informed the answer"
    )
    
    # Entity information
    entities: EntityInfo = Field(
        default_factory=EntityInfo,
        description="Structured information about entities mentioned in the answer"
    )
    
    # Additional structured data
    structured_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Any additional structured data extracted from the answer"
    )
    
    # Metadata about query processing
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Processing metadata like query type, confidence, timing, etc."
    )

    answer: str = Field(..., description="The final answer to the user's query")
    
    model_config = {"validate_assignment": True} 