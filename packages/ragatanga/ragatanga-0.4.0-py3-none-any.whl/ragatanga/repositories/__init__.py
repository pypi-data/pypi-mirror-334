"""
Ragatanga Repository Layer

This package contains repository classes for database persistence.
Repositories provide an abstraction layer between the domain models and the database.
"""

from ragatanga.repositories.base import BaseRepository
from ragatanga.repositories.tenant import TenantRepository
from ragatanga.repositories.ontology import OntologyRepository
from ragatanga.repositories.knowledge_base import KnowledgeBaseRepository

__all__ = [
    "BaseRepository",
    "TenantRepository",
    "OntologyRepository",
    "KnowledgeBaseRepository"
] 