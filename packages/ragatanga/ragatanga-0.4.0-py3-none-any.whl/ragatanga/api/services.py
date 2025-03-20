"""
Service layer for Ragatanga API.

This module contains services that encapsulate business logic for the API.
"""

from typing import Optional
from loguru import logger
import time
import traceback

from ragatanga.exceptions import ConfigurationError
from ragatanga.core.owl_retriever import UniversalOntologyManager
from ragatanga.core.semantic import SemanticSearch
from ragatanga.core.query import generate_structured_answer
from ragatanga.core.retrievers import (
    SemanticRetriever,
    OntologyRetriever,
    RetrievalOrchestrator
)
from ragatanga.core.models import QueryResponse


class QueryService:
    """Service for handling query processing and retrieval."""
    
    def __init__(
        self,
        ontology_manager: Optional[UniversalOntologyManager] = None,
        semantic_search: Optional[SemanticSearch] = None
    ):
        """
        Initialize the query service.
        
        Args:
            ontology_manager: Tenant-specific ontology manager
            semantic_search: Semantic search instance
        """
        # Create specialized retrievers
        self.semantic_retriever = SemanticRetriever(semantic_search)
        self.ontology_retriever = OntologyRetriever(ontology_manager)
        
        # Create the orchestrator
        self.orchestrator = RetrievalOrchestrator(
            semantic_retriever=self.semantic_retriever,
            ontology_retriever=self.ontology_retriever
        )
        
        # Store dependencies for validation
        self.ontology_manager = ontology_manager
        self.semantic_search = semantic_search
    
    async def process_query(self, tenant_id: str, query: str) -> QueryResponse:
        """
        Process a query for a specific tenant.
        
        Args:
            tenant_id: Tenant ID
            query: User query
            
        Returns:
            QueryResponse with answer and retrieved facts
            
        Raises:
            ConfigurationError: If required components are not configured
        """
        # Validate configuration
        self._validate_configuration(tenant_id)
        
        # Log the query
        logger.info(f"Processing query for tenant {tenant_id}: {query}")
        
        # Track processing time
        start_time = time.time()
        
        try:
            # Get categorized results from all sources
            results = await self.orchestrator.retrieve(query)
            
            # Extract the separate result lists directly
            sparql_results = results.get('sparql', [])
            semantic_results = results.get('semantic', [])
            
            # Generate a structured answer
            logger.debug(f"Generating answer with {len(sparql_results)} SPARQL results and {len(semantic_results)} semantic results")
            
            response = await generate_structured_answer(
                query=query, 
                sparql_results=sparql_results,
                semantic_results=semantic_results
            )
            
            # Add processing time to metadata
            elapsed_time = time.time() - start_time
            response.metadata["processing_time_seconds"] = elapsed_time
            logger.info(f"Query processed in {elapsed_time:.2f} seconds")
            
            return response
            
        except Exception as e:
            # Log detailed error
            error_detail = traceback.format_exc()
            logger.error(f"Error processing query for tenant {tenant_id}: {str(e)}\n{error_detail}")
            
            # Re-raise the exception to be handled by the route handler
            raise
    
    def _validate_configuration(self, tenant_id: str) -> None:
        """
        Validate that at least one retrieval method is configured.
        
        Args:
            tenant_id: Tenant ID
            
        Raises:
            ConfigurationError: If no retrieval methods are configured
        """
        if not self.ontology_manager and not self.semantic_search:
            raise ConfigurationError(
                message="No retrieval methods configured",
                detailed_message="Neither ontology nor semantic search is configured for this tenant. Please configure at least one retrieval method.",
                error_code="no_retrieval_methods"
            ) 