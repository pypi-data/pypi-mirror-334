"""
Tenant management for Ragatanga.

This module provides classes and functionality for managing tenant-specific 
ontologies and knowledge bases.
"""

import os
from typing import Dict, Optional
from loguru import logger

from ragatanga.core.owl_retriever import UniversalOntologyManager
from ragatanga.core.semantic import SemanticSearch
from ragatanga.core.retrievers import SemanticRetriever, OntologyRetriever, RetrievalOrchestrator
from ragatanga.models.tenant import tenant_store
from ragatanga.config import DATA_DIR


class TenantOntologyManager:
    """
    Manager for tenant-specific ontologies.
    
    This class manages ontology instances for each tenant,
    handling initialization, reloading, and access.
    """
    
    def __init__(self):
        """Initialize the tenant ontology manager."""
        self._ontology_managers: Dict[str, UniversalOntologyManager] = {}
    
    async def initialize(self):
        """
        Initialize ontology managers for all tenants.
        
        This method should be called during application startup
        to load all tenant ontologies.
        """
        logger.info("Initializing tenant ontology managers")
        for tenant in tenant_store.list_tenants():
            try:
                ontology = tenant_store.get_active_ontology(tenant.id)
                if ontology and os.path.exists(ontology.file_path):
                    logger.info(f"Loading ontology for tenant {tenant.id}: {ontology.file_path}")
                    
                    # Create backend path in tenant directory
                    tenant_dir = os.path.join(DATA_DIR, "tenants", tenant.id)
                    os.makedirs(tenant_dir, exist_ok=True)
                    
                    # Create a dedicated backend for this tenant's ontology
                    ontology_name = os.path.basename(ontology.file_path).split('.')[0]
                    backend_path = os.path.join(tenant_dir, f"{ontology_name}_world.sqlite3")
                    
                    # Create the manager with persistent backend
                    manager = UniversalOntologyManager(
                        ontology_path=ontology.file_path,
                        backend_path=backend_path
                    )
                    
                    # Load the ontology (will use backend if available)
                    await manager.load_and_materialize()
                    self._ontology_managers[tenant.id] = manager
                    
                    # Update last_used timestamp
                    tenant_store.update_ontology_last_used(tenant.id, ontology.id)
                    
                    logger.info(f"Successfully loaded ontology for tenant {tenant.id}")
                else:
                    logger.warning(f"No active ontology found for tenant {tenant.id}")
            except Exception as e:
                logger.error(f"Error loading ontology for tenant {tenant.id}: {str(e)}")
                logger.exception("Exception details:")
        
        logger.info(f"Initialized ontology managers for {len(self._ontology_managers)} tenants")
    
    def get_ontology_manager(self, tenant_id: str) -> Optional[UniversalOntologyManager]:
        """
        Get the ontology manager for a specific tenant.
        
        Args:
            tenant_id: The tenant ID
            
        Returns:
            The tenant's ontology manager or None if not found
        """
        return self._ontology_managers.get(tenant_id)
    
    async def reload_ontology(self, tenant_id: str, force_rebuild: bool = False) -> bool:
        """
        Reload the ontology for a specific tenant.
        
        Args:
            tenant_id: The tenant ID
            force_rebuild: Whether to force rebuilding indexes
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the tenant's active ontology
            ontology = tenant_store.get_active_ontology(tenant_id)
            if not ontology:
                logger.warning(f"No active ontology found for tenant {tenant_id}")
                return False
            
            if not os.path.exists(ontology.file_path):
                logger.error(f"Ontology file not found for tenant {tenant_id}: {ontology.file_path}")
                return False
            
            # Create tenant directory if it doesn't exist
            tenant_dir = os.path.join(DATA_DIR, "tenants", tenant_id)
            os.makedirs(tenant_dir, exist_ok=True)
            
            # Determine backend path
            ontology_name = os.path.basename(ontology.file_path).split('.')[0]
            backend_path = os.path.join(tenant_dir, f"{ontology_name}_world.sqlite3")
            
            # Create or get the ontology manager
            manager = self._ontology_managers.get(tenant_id)
            if not manager:
                # Create a new manager with persistent backend
                manager = UniversalOntologyManager(
                    ontology_path=ontology.file_path,
                    backend_path=backend_path
                )
                self._ontology_managers[tenant_id] = manager
            else:
                # Update paths if changed
                manager.ontology_path = ontology.file_path
                manager.backend_path = backend_path
                
                # If not force_rebuild and backend exists, we'll try to use it
                if not force_rebuild and os.path.exists(backend_path):
                    # File hasn't changed since last save, we could skip full reload
                    # But we'll let the manager handle this logic
                    pass
            
            # Reload the ontology (will use backend if appropriate)
            result = await manager.load_and_materialize(force_rebuild=force_rebuild)
            
            # Save the world state if loaded successfully
            if result and manager.loaded:
                manager.save()  # Save world state to backend
                
            # Update last_used timestamp
            tenant_store.update_ontology_last_used(tenant_id, ontology.id)
            
            logger.info(f"Successfully {'reloaded' if result else 'failed to reload'} ontology for tenant {tenant_id}")
            return result
        except Exception as e:
            logger.error(f"Error reloading ontology for tenant {tenant_id}: {str(e)}")
            logger.exception("Exception details:")
            return False


class TenantKnowledgeBaseManager:
    """
    Manager for tenant-specific knowledge bases.
    
    This class manages semantic search instances for each tenant,
    handling initialization, reloading, and access.
    """
    
    def __init__(self):
        """Initialize the tenant knowledge base manager."""
        self._semantic_searches: Dict[str, SemanticSearch] = {}
    
    async def initialize(self):
        """
        Initialize semantic search instances for all tenants.
        
        This method should be called during application startup
        to load all tenant knowledge bases.
        """
        logger.info("Initializing tenant knowledge base managers")
        for tenant in tenant_store.list_tenants():
            try:
                kb = tenant_store.get_active_knowledge_base(tenant.id)
                if kb and os.path.exists(kb.file_path):
                    logger.info(f"Loading knowledge base for tenant {tenant.id}: {kb.file_path}")
                    semantic_search = SemanticSearch()
                    await semantic_search.load_knowledge_base(kb.file_path, force_rebuild=False)
                    self._semantic_searches[tenant.id] = semantic_search
                    
                    # Update last_used timestamp
                    tenant_store.update_kb_last_used(tenant.id, kb.id)
                    
                    logger.info(f"Successfully loaded knowledge base for tenant {tenant.id}")
                else:
                    logger.warning(f"No active knowledge base found for tenant {tenant.id}")
            except Exception as e:
                logger.error(f"Error loading knowledge base for tenant {tenant.id}: {str(e)}")
                logger.exception("Exception details:")
        
        logger.info(f"Initialized knowledge base managers for {len(self._semantic_searches)} tenants")
    
    def get_semantic_search(self, tenant_id: str) -> Optional[SemanticSearch]:
        """
        Get the semantic search instance for a specific tenant.
        
        Args:
            tenant_id: The tenant ID
            
        Returns:
            The tenant's semantic search instance or None if not found
        """
        return self._semantic_searches.get(tenant_id)
    
    async def reload_knowledge_base(self, tenant_id: str, force_rebuild: bool = False) -> bool:
        """
        Reload the knowledge base for a specific tenant.
        
        Args:
            tenant_id: The tenant ID
            force_rebuild: Whether to force rebuilding indexes
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the tenant's active knowledge base
            kb = tenant_store.get_active_knowledge_base(tenant_id)
            if not kb:
                logger.warning(f"No active knowledge base found for tenant {tenant_id}")
                return False
            
            if not os.path.exists(kb.file_path):
                logger.error(f"Knowledge base file not found for tenant {tenant_id}: {kb.file_path}")
                return False
            
            # Create or get the semantic search instance
            semantic_search = self._semantic_searches.get(tenant_id)
            if not semantic_search:
                semantic_search = SemanticSearch()
                self._semantic_searches[tenant_id] = semantic_search
            
            # Reload the knowledge base
            await semantic_search.load_knowledge_base(kb.file_path, force_rebuild=force_rebuild)
            
            # Update last_used timestamp
            tenant_store.update_kb_last_used(tenant_id, kb.id)
            
            logger.info(f"Successfully reloaded knowledge base for tenant {tenant_id}")
            return True
        except Exception as e:
            logger.error(f"Error reloading knowledge base for tenant {tenant_id}: {str(e)}")
            logger.exception("Exception details:")
            return False


class TenantRetrieverManager:
    """
    Manager for tenant-specific retrieval components.
    
    This class manages retriever instances for each tenant,
    combining ontology and semantic search functionality.
    """
    
    def __init__(self):
        """Initialize the tenant retriever manager."""
        self._retrievers: Dict[str, RetrievalOrchestrator] = {}
    
    async def initialize(self):
        """
        Initialize retrievers for all tenants.
        
        This method should be called during application startup
        to create retrievers for all tenants.
        """
        logger.info("Initializing tenant retrievers")
        for tenant in tenant_store.list_tenants():
            try:
                # Get tenant's ontology manager
                ontology_manager = tenant_ontology_manager.get_ontology_manager(tenant.id)
                
                # Get tenant's semantic search
                semantic_search = tenant_kb_manager.get_semantic_search(tenant.id)
                
                if ontology_manager or semantic_search:
                    # Create ontology retriever if we have an ontology manager
                    ontology_retriever = None
                    if ontology_manager:
                        ontology_retriever = OntologyRetriever(
                            ontology_manager=ontology_manager
                        )
                    
                    # Create semantic retriever if we have semantic search
                    semantic_retriever = None
                    if semantic_search:
                        semantic_retriever = SemanticRetriever(
                            semantic_search=semantic_search
                        )
                    
                    # Create the orchestrator with available retrievers
                    orchestrator = RetrievalOrchestrator(
                        semantic_retriever=semantic_retriever,
                        ontology_retriever=ontology_retriever
                    )
                    
                    self._retrievers[tenant.id] = orchestrator
                    logger.info(f"Created retriever for tenant {tenant.id}")
            except Exception as e:
                logger.error(f"Error creating retriever for tenant {tenant.id}: {str(e)}")
    
    def get_retriever(self, tenant_id: str) -> Optional[RetrievalOrchestrator]:
        """
        Get the retriever for a specific tenant.
        
        Args:
            tenant_id: Tenant ID
            
        Returns:
            The tenant's retriever or None if not configured
        """
        return self._retrievers.get(tenant_id)


# Global singleton instances
tenant_ontology_manager = TenantOntologyManager()
tenant_kb_manager = TenantKnowledgeBaseManager()
tenant_retriever_manager = TenantRetrieverManager()


async def setup_default_tenant() -> None:
    """
    Set up the default tenant with sample data files.
    Note: This function will not create a new tenant, only add sample data
    to an existing default tenant.
    """
    if not tenant_store.default_tenant:
        logger.warning("No default tenant found, cannot set up default resources")
        return
        
    default_id = tenant_store.default_tenant.id
    logger.info(f"Setting up default tenant with ID: {default_id}")
    
    # Check if the tenant already has an ontology
    existing_ontology = tenant_store.get_active_ontology(default_id)
    if existing_ontology:
        logger.info(f"Default tenant already has an active ontology: {existing_ontology.name}")
    else:
        # Add sample ontology to default tenant
        sample_ontology_path = os.path.join(DATA_DIR, "sample_ontology_owl.ttl")
        if os.path.exists(sample_ontology_path):
            logger.info(f"Adding sample ontology to default tenant from: {sample_ontology_path}")
            tenant_store.add_ontology(
                tenant_id=default_id,
                name="Sample Ontology",
                file_path=sample_ontology_path,
                description="Default sample ontology provided with Ragatanga"
            )
        else:
            logger.warning(f"Sample ontology file not found at: {sample_ontology_path}")
    
    # Check if the tenant already has a knowledge base
    existing_kb = tenant_store.get_active_knowledge_base(default_id)
    if existing_kb:
        logger.info(f"Default tenant already has an active knowledge base: {existing_kb.name}")
    else:
        # Add sample knowledge base to default tenant
        sample_kb_path = os.path.join(DATA_DIR, "sample_knowledge_base.md")
        if os.path.exists(sample_kb_path):
            logger.info(f"Adding sample knowledge base to default tenant from: {sample_kb_path}")
            tenant_store.add_knowledge_base(
                tenant_id=default_id,
                name="Sample Knowledge Base",
                file_path=sample_kb_path,
                description="Default sample knowledge base provided with Ragatanga"
            )
        else:
            logger.warning(f"Sample knowledge base file not found at: {sample_kb_path}")
    
    # Make sure the ontology is loaded
    ont_manager = tenant_ontology_manager.get_ontology_manager(default_id)
    if ont_manager is None:
        logger.info("Initializing ontology manager for default tenant")
        await tenant_ontology_manager.reload_ontology(default_id, force_rebuild=True)
    elif not (hasattr(ont_manager, 'loaded') and ont_manager.loaded):
        logger.info("Reloading ontology for default tenant")
        await tenant_ontology_manager.reload_ontology(default_id, force_rebuild=True)
    else:
        logger.info("Ontology manager for default tenant is already loaded")
        
    # Make sure the knowledge base is loaded
    kb_search = tenant_kb_manager.get_semantic_search(default_id)
    if kb_search is None:
        logger.info("Initializing knowledge base for default tenant")
        await tenant_kb_manager.reload_knowledge_base(default_id, force_rebuild=True)
    else:
        logger.info("Knowledge base for default tenant is already loaded")
        
    # Finally, make sure a retriever is set up for this tenant
    retriever = tenant_retriever_manager.get_retriever(default_id)
    if retriever is None:
        # Get the updated managers after reloading
        ont_manager = tenant_ontology_manager.get_ontology_manager(default_id)
        kb_search = tenant_kb_manager.get_semantic_search(default_id)
        
        if ont_manager and kb_search:
            logger.info("Setting up retriever for default tenant")
            # Create a new retriever and add it to the manager
            try:
                # Create retrievers for ontology and semantic search
                ontology_retriever = OntologyRetriever(ontology_manager=ont_manager)
                semantic_retriever = SemanticRetriever(semantic_search=kb_search)
                
                # Create the orchestrator
                new_retriever = RetrievalOrchestrator(
                    semantic_retriever=semantic_retriever,
                    ontology_retriever=ontology_retriever
                )
                tenant_retriever_manager._retrievers[default_id] = new_retriever
                logger.info("Successfully created retriever for default tenant")
            except Exception as e:
                logger.error(f"Error creating retriever for default tenant: {str(e)}")
        else:
            logger.warning("Cannot create retriever - missing dependencies")
    else:
        logger.info("Retriever for default tenant is already set up") 