"""
Tenant models for Ragatanga.

This module defines the data models for tenant management and isolation.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Literal
from pydantic import BaseModel, Field


class Tenant(BaseModel):
    """Tenant model representing a company or organization."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def custom_dict(self) -> Dict[str, Any]:
        """Convert the tenant to a dictionary with formatted dates."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
        }


class TenantOntology(BaseModel):
    """Model representing a tenant's ontology."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    name: str
    file_path: str
    description: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True


class TenantKnowledgeBase(BaseModel):
    """Model representing a tenant's knowledge base."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    name: str
    file_path: str
    description: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True


class TenantStore:
    """
    Global store for tenant data.
    
    This class manages tenants, ontologies, and knowledge bases in memory.
    In a production system, this would be replaced with a database.
    """
    
    def __init__(self):
        """Initialize the tenant store."""
        self.tenants: Dict[str, Tenant] = {}
        self.ontologies: Dict[str, TenantOntology] = {}
        self.knowledge_bases: Dict[str, TenantKnowledgeBase] = {}
        self.default_tenant: Optional[Tenant] = None
    
    def create_tenant(self, name: str, metadata: Optional[Dict[str, Any]] = None) -> Tenant:
        """
        Create a new tenant.
        
        Args:
            name: The tenant name
            metadata: Optional metadata
            
        Returns:
            The created tenant
        """
        tenant = Tenant(
            name=name,
            metadata=metadata or {}
        )
        self.tenants[tenant.id] = tenant
        
        # Set as default if first tenant
        if not self.default_tenant:
            self.default_tenant = tenant
        
        return tenant
    
    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """
        Get a tenant by ID.
        
        Args:
            tenant_id: The tenant ID
            
        Returns:
            The tenant or None if not found
        """
        return self.tenants.get(tenant_id)
    
    def list_tenants(self) -> List[Tenant]:
        """
        List all tenants.
        
        Returns:
            List of tenants
        """
        return list(self.tenants.values())
    
    def add_ontology(
        self, 
        tenant_id: str, 
        name: str, 
        file_path: str, 
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TenantOntology:
        """
        Add an ontology to a tenant.
        
        Args:
            tenant_id: The tenant ID
            name: The ontology name
            file_path: Path to the ontology file
            description: Optional description
            metadata: Optional metadata
            
        Returns:
            The created ontology
        """
        # Deactivate existing ontologies for this tenant
        for ont in self.ontologies.values():
            if ont.tenant_id == tenant_id and ont.is_active:
                ont.is_active = False
        
        # Create new ontology
        ontology = TenantOntology(
            tenant_id=tenant_id,
            name=name,
            file_path=file_path,
            description=description,
            metadata=metadata or {}
        )
        self.ontologies[ontology.id] = ontology
        
        return ontology
    
    def get_active_ontology(self, tenant_id: str) -> Optional[TenantOntology]:
        """
        Get the active ontology for a tenant.
        
        Args:
            tenant_id: The tenant ID
            
        Returns:
            The active ontology or None
        """
        for ont in self.ontologies.values():
            if ont.tenant_id == tenant_id and ont.is_active:
                return ont
        return None
    
    def add_knowledge_base(
        self, 
        tenant_id: str, 
        name: str, 
        file_path: str, 
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TenantKnowledgeBase:
        """
        Add a knowledge base to a tenant.
        
        Args:
            tenant_id: The tenant ID
            name: The knowledge base name
            file_path: Path to the knowledge base file
            description: Optional description
            metadata: Optional metadata
            
        Returns:
            The created knowledge base
        """
        # Deactivate existing knowledge bases for this tenant
        for kb in self.knowledge_bases.values():
            if kb.tenant_id == tenant_id and kb.is_active:
                kb.is_active = False
        
        # Create new knowledge base
        knowledge_base = TenantKnowledgeBase(
            tenant_id=tenant_id,
            name=name,
            file_path=file_path,
            description=description,
            metadata=metadata or {}
        )
        self.knowledge_bases[knowledge_base.id] = knowledge_base
        
        return knowledge_base
    
    def get_active_knowledge_base(self, tenant_id: str) -> Optional[TenantKnowledgeBase]:
        """
        Get the active knowledge base for a tenant.
        
        Args:
            tenant_id: The tenant ID
            
        Returns:
            The active knowledge base or None
        """
        for kb in self.knowledge_bases.values():
            if kb.tenant_id == tenant_id and kb.is_active:
                return kb
        return None
    
    def update_ontology_last_used(self, tenant_id: str, ontology_id: str) -> bool:
        """
        Update the last_used timestamp of an ontology.
        
        Args:
            tenant_id: The tenant ID
            ontology_id: The ontology ID
            
        Returns:
            True if successful, False if not found
        """
        ontology = self.ontologies.get(ontology_id)
        if ontology and ontology.tenant_id == tenant_id:
            ontology.last_used = datetime.now()
            return True
        return False
    
    def update_kb_last_used(self, tenant_id: str, kb_id: str) -> bool:
        """
        Update the last_used timestamp of a knowledge base.
        
        Args:
            tenant_id: The tenant ID
            kb_id: The knowledge base ID
            
        Returns:
            True if successful, False if not found
        """
        kb = self.knowledge_bases.get(kb_id)
        if kb and kb.tenant_id == tenant_id:
            kb.last_used = datetime.now()
            return True
        return False


# Global tenant store singleton
tenant_store = TenantStore()