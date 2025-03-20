"""
Retrieval implementations for Ragatanga.

This module provides the base retriever interface and concrete implementations
for different retrieval strategies.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import json

from loguru import logger

from ragatanga.core.owl_retriever import UniversalOntologyManager
from ragatanga.core.semantic import SemanticSearch
from ragatanga.utils.sparql import generate_sparql_query


class BaseRetriever(ABC):
    """Base interface for all retrievers."""
    
    @abstractmethod
    async def retrieve(self, query: str) -> List[str]:
        """
        Retrieve relevant information for a query.
        
        Args:
            query: The user query
            
        Returns:
            List of retrieval results as strings
        """
        pass


class SemanticRetriever(BaseRetriever):
    """Retrieves information using semantic search."""
    
    def __init__(self, semantic_search: Optional[SemanticSearch] = None):
        """
        Initialize the semantic retriever.
        
        Args:
            semantic_search: The semantic search instance to use
        """
        self.semantic_search = semantic_search
    
    async def retrieve(self, query: str) -> List[str]:
        """
        Retrieve information using semantic search.
        
        Args:
            query: The user query
            
        Returns:
            List of semantically relevant text passages
        """
        if not self.semantic_search:
            logger.warning("Semantic search not configured")
            return []
        
        try:
            # Use the search method which returns a list of strings
            results = await self.semantic_search.search(query)
            logger.info(f"Retrieved {len(results)} semantic results")
            return results
        except Exception as e:
            logger.error(f"Error in semantic retrieval: {str(e)}")
            return []


class OntologyRetriever(BaseRetriever):
    """Retrieves information using SPARQL queries against an ontology."""
    
    def __init__(self, ontology_manager: Optional[UniversalOntologyManager] = None):
        """
        Initialize the ontology retriever.
        
        Args:
            ontology_manager: The ontology manager instance to use
        """
        self.ontology_manager = ontology_manager
    
    async def retrieve(self, query: str, parameters: Optional[List] = None) -> List[str]:
        """
        Retrieve information using SPARQL queries.
        
        Args:
            query: The user query
            parameters: Optional parameters for parameterized SPARQL queries
            
        Returns:
            List of SPARQL query results as strings
        """
        if not self.ontology_manager:
            logger.warning("Ontology manager not configured")
            return []
        
        try:
            # Get the ontology schema for SPARQL query generation
            schema = self.ontology_manager.get_ontology_structure()
            
            # Convert schema to string for the generator
            schema_str = json.dumps(schema)
            
            # Generate SPARQL query using the utility function
            sparql_query = await generate_sparql_query(query, schema_str, parameters=parameters)
            
            if not sparql_query:
                logger.warning(f"Failed to generate SPARQL query for: {query}")
                return []
            
            # Execute the query
            results = await self.ontology_manager.execute_query(sparql_query, parameters)
            logger.info(f"Retrieved {len(results)} SPARQL results")
            return [self._format_result(r) for r in results]
        except Exception as e:
            logger.error(f"Error in ontology retrieval: {str(e)}")
            return []
    
    def _format_result(self, result: Any) -> str:
        """Format a SPARQL result as a string."""
        if isinstance(result, dict):
            return ", ".join(f"{k}: {v}" for k, v in result.items() if v)
        return str(result)


class RetrievalOrchestrator:
    """Orchestrates multiple retrievers without complex merging."""
    
    def __init__(
        self,
        semantic_retriever: Optional[SemanticRetriever] = None,
        ontology_retriever: Optional[OntologyRetriever] = None
    ):
        """
        Initialize with specific retrievers.
        
        Args:
            semantic_retriever: Retriever for semantic search
            ontology_retriever: Retriever for ontology/SPARQL queries
        """
        self.semantic_retriever = semantic_retriever
        self.ontology_retriever = ontology_retriever
    
    async def retrieve(self, query: str) -> Dict[str, List[str]]:
        """
        Retrieve from all sources.
        
        Args:
            query: The user query
            
        Returns:
            Dictionary with 'semantic' and 'sparql' keys mapping to respective results
        """
        results: Dict[str, List[str]] = {
            'semantic': [],
            'sparql': []
        }
        
        # Get SPARQL results if available
        if self.ontology_retriever:
            try:
                results['sparql'] = await self.ontology_retriever.retrieve(query)
            except Exception as e:
                logger.error(f"Error in ontology retrieval: {str(e)}")
        
        # Get semantic results if available
        if self.semantic_retriever:
            try:
                results['semantic'] = await self.semantic_retriever.retrieve(query)
            except Exception as e:
                logger.error(f"Error in semantic retrieval: {str(e)}")
        
        return results 