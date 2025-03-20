"""
Ragatanga - A hybrid knowledge retrieval system that combines ontology-based reasoning
with semantic search for powerful knowledge retrieval.
"""

__version__ = "0.4.0"

# Make core components available at package level
from ragatanga.core.owl_retriever import UniversalOntologyManager
from ragatanga.core.retrievers import SemanticRetriever, OntologyRetriever, RetrievalOrchestrator
from ragatanga.core.semantic import SemanticSearch
from ragatanga.core.query import generate_structured_answer

# Make schema models available at package level
from ragatanga.schemas import (
    Tenant, TenantCreate, TenantUpdate,
    Ontology, OntologyCreate, OntologyUpdate, OntologyStats,
    KnowledgeBase, KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseStats,
    Query, QueryResult, QueryConfig, QueryType
)

__all__ = [
    # Version
    "__version__",
    
    # Core components
    "UniversalOntologyManager",
    "SemanticRetriever",
    "OntologyRetriever",
    "RetrievalOrchestrator",
    "SemanticSearch",
    "generate_structured_answer",
    
    # Schema models
    "Tenant", "TenantCreate", "TenantUpdate",
    "Ontology", "OntologyCreate", "OntologyUpdate", "OntologyStats",
    "KnowledgeBase", "KnowledgeBaseCreate", "KnowledgeBaseUpdate", "KnowledgeBaseStats",
    "Query", "QueryResult", "QueryConfig", "QueryType"
]