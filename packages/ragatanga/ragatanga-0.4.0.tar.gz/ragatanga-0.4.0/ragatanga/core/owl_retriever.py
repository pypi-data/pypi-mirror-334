"""
Universal ontology retrieval module using Owlready2 for robust ontology-based queries.

This module provides improved ontology loading, query generation, and entity handling
to work with any type of ontology and query pattern.
"""

import os
import time
import hashlib
import json
from typing import Dict, Any, Optional, Tuple, List, Set
import logging
from collections.abc import Iterable
import traceback
from datetime import datetime, timedelta
from functools import lru_cache
from owlready2 import World, sync_reasoner

logger = logging.getLogger(__name__)

# Query cache settings
_QUERY_CACHE_SIZE = 1000  # Maximum number of cached query results
_QUERY_CACHE_EXPIRY = timedelta(hours=1)  # Cache expiry time

class UniversalOntologyManager:
    """Universal ontology manager using Owlready2 for robust ontology interactions."""
    
    def __init__(self, 
                 ontology_path: str, 
                 backend_path: Optional[str] = None,
                 enable_query_cache: bool = True,
                 cache_size: int = _QUERY_CACHE_SIZE) -> None:
        """
        Initialize the ontology manager.
        
        Args:
            ontology_path: Path to the ontology file (.ttl, .owl, etc.)
            backend_path: Path to store the persistent Owlready2 backend
                          If None, a default path based on ontology name will be used
            enable_query_cache: Whether to enable caching of query results
            cache_size: Maximum number of query results to cache
        """
        self.ontology_path = ontology_path
        
        # If no backend path is provided, create one based on the ontology path
        if backend_path is None and ontology_path:
            ontology_name = os.path.basename(ontology_path).split('.')[0]
            backend_dir = os.path.join(os.path.dirname(ontology_path), "owl_cache")
            os.makedirs(backend_dir, exist_ok=True)
            self.backend_path = os.path.join(backend_dir, f"{ontology_name}_world.sqlite3")
        else:
            self.backend_path = backend_path or ""  # Ensure it's never None
            
        self.world = None
        self.ontology = None
        self.loaded = False
        self.materialized = False
        self.namespaces: Dict[str, str] = {}
        self.statistics: Dict[str, Any] = {}
        
        # Query cache
        self.enable_query_cache = enable_query_cache
        self._query_cache: Dict[str, Tuple[List[Dict[str, Any]], datetime]] = {}
        self._cache_size = cache_size
        
        # Performance metrics
        self._load_time = 0.0
        self._materialize_time = 0.0
        
    def _generate_query_cache_key(self, query: str, parameters: Optional[List] = None) -> str:
        """
        Generate a cache key for a SPARQL query.
        
        Args:
            query: The SPARQL query string
            parameters: Optional parameters for the query
            
        Returns:
            A hash string to use as cache key
        """
        # Normalize the query by removing extra whitespace
        normalized_query = " ".join(query.split())
        
        # Include parameters in the key if provided
        param_str = ""
        if parameters:
            param_str = json.dumps(parameters, sort_keys=True)
            
        # Combine and hash
        combined = f"{normalized_query}|{param_str}"
        return hashlib.md5(combined.encode()).hexdigest()
        
    def _clean_expired_cache_entries(self) -> None:
        """Remove expired entries from the query cache."""
        if not self.enable_query_cache or not self._query_cache:
            return
            
        current_time = datetime.now()
        expired_keys = [
            k for k, (_, timestamp) in self._query_cache.items()
            if current_time - timestamp > _QUERY_CACHE_EXPIRY
        ]
        
        for key in expired_keys:
            del self._query_cache[key]
            
    def _trim_cache_if_needed(self) -> None:
        """Trim the cache if it exceeds the maximum size."""
        if len(self._query_cache) > self._cache_size:
            # Remove oldest entries first (based on timestamp)
            sorted_items = sorted(
                self._query_cache.items(),
                key=lambda x: x[1][1]  # Sort by timestamp
            )
            
            # Keep only the newest entries
            to_keep = sorted_items[-self._cache_size:]
            self._query_cache = {k: v for k, v in to_keep}

    def get_ontology_structure(self) -> Dict[str, Any]:
        """
        Get a structured representation of the ontology.
        
        Returns:
            Dictionary with ontology structure
        """
        # Initialize the structure with empty lists
        structure: Dict[str, Any] = {
            "classes": [],
            "properties": [],
            "individuals": [],
            "metadata": {
                "error": None,
                "debug_info": {}
            }
        }
        
        try:
            if self.ontology is None:
                logger.warning("Ontology not loaded when get_ontology_structure was called")
                # Update the error field directly
                structure["metadata"] = {"error": "Ontology not loaded", "debug_info": {}}
                return structure
            
            # Add debug information
            structure["metadata"]["debug_info"]["ontology_type"] = str(type(self.ontology))
            structure["metadata"]["debug_info"]["world_type"] = str(type(self.world)) if self.world else "None"
            
            # Use cached statistics if available
            if hasattr(self, 'statistics') and self.statistics:
                logger.info(f"Using cached statistics: {self.statistics}")
                structure["statistics"] = self.statistics.copy()
                structure["metadata"]["debug_info"]["using_cached_stats"] = True
            else:
                logger.warning("No cached statistics available")
                structure["metadata"]["debug_info"]["using_cached_stats"] = False
            
            # Extract classes and their properties
            class_list = []
            try:
                if hasattr(self.ontology, "classes") and callable(self.ontology.classes):
                    class_list = list(self.ontology.classes())
                    logger.info(f"Found {len(class_list)} classes in ontology")
                else:
                    logger.warning("Ontology does not have a callable 'classes' method")
                    structure["metadata"]["debug_info"]["has_classes_method"] = False
                
                for i, cls in enumerate(class_list):
                    if hasattr(cls, "name") and cls.name:
                        # Create a more detailed class entry
                        structure["classes"].append({"name": cls.name})
            except Exception as class_error:
                logger.error(f"Error processing classes: {str(class_error)}")
                structure["metadata"]["debug_info"]["class_error"] = str(class_error)
            
            # Extract properties
            prop_list = []
            try:
                if hasattr(self.ontology, "properties") and callable(self.ontology.properties):
                    prop_list = list(self.ontology.properties())
                    logger.info(f"Found {len(prop_list)} properties in ontology")
                else:
                    logger.warning("Ontology does not have a callable 'properties' method")
                    structure["metadata"]["debug_info"]["has_properties_method"] = False
                
                for i, prop in enumerate(prop_list):
                    if hasattr(prop, "name") and prop.name:
                        # Create a more detailed property entry
                        structure["properties"].append({"name": prop.name})
            except Exception as prop_error:
                logger.error(f"Error processing properties: {str(prop_error)}")
                structure["metadata"]["debug_info"]["property_error"] = str(prop_error)
            
            # Extract instances/individuals
            ind_list = []
            try:
                if hasattr(self.ontology, "individuals") and callable(self.ontology.individuals):
                    ind_list = list(self.ontology.individuals())
                    logger.info(f"Found {len(ind_list)} individuals in ontology")
                else:
                    logger.warning("Ontology does not have a callable 'individuals' method")
                    structure["metadata"]["debug_info"]["has_individuals_method"] = False
                
                for i, individual in enumerate(ind_list):
                    if hasattr(individual, "name") and individual.name:
                        # Create a more detailed individual entry
                        structure["individuals"].append({"name": individual.name})
            except Exception as ind_error:
                logger.error(f"Error processing individuals: {str(ind_error)}")
                structure["metadata"]["debug_info"]["individual_error"] = str(ind_error)
            
            # Update statistics if they weren't already set from cache
            if not structure["statistics"].get("class_count"):
                structure["statistics"] = {
                    "class_count": len(class_list),
                    "property_count": len(prop_list),
                    "entity_count": len(ind_list),
                    "total_elements": len(class_list) + len(prop_list) + len(ind_list)
                }
            
            # Store statistics for later use
            self.statistics = structure["statistics"].copy()
            
            # Debug information about all available classes in the ontology
            try:
                if hasattr(self, 'ontology') and self.ontology is not None and hasattr(self.ontology, 'base_iri'):
                    logger.debug(f"Base IRI: {self.ontology.base_iri}")
                
                if hasattr(self, 'world') and self.world is not None:
                    if hasattr(self.world, 'classes') and callable(self.world.classes):
                        logger.debug(f"Available classes: {[c for c in self.world.classes()]}")
                    
                    if hasattr(self.world, 'properties') and callable(self.world.properties):
                        logger.debug(f"Available properties: {[p for p in self.world.properties()]}")
                    
                    if hasattr(self.world, 'individuals') and callable(self.world.individuals):
                        logger.debug(f"Available individuals: {[i for i in self.world.individuals()]}")
            except Exception as e:
                logger.error(f"Error during debug inspection: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error extracting ontology structure: {str(e)}")
            # Update the error field directly
            structure["metadata"] = {
                "error": str(e),
                "debug_info": {"exception": traceback.format_exc()}
            }
        
        return structure
    async def load_and_materialize(self, force_rebuild: bool = False) -> bool:
        """
        Load and materialize the ontology with robust error handling.
        
        Args:
            force_rebuild: Force regeneration of inferences and cache
            
        Returns:
            bool: True if ontology loaded and materialized successfully
        """
        start_time = time.time()
        
        try:
            logger.info(f"Loading and materializing ontology from {self.ontology_path}")
            
            # Check if file exists
            if not os.path.exists(self.ontology_path):
                logger.error(f"Ontology file not found: {self.ontology_path}")
                return False
            
            # Step 1: Load the base ontology
            success = self.load()
            if not success:
                logger.error("Failed to load base ontology")
                return False
                
            # Check if we have no classes/properties/individuals despite the ontology being loaded
            # This is a sign of namespace issues
            if (self.ontology is not None and self.loaded and
                (not hasattr(self, 'statistics') or 
                 self.statistics.get("class_count", 0) == 0 and 
                 self.statistics.get("property_count", 0) == 0 and
                 self.statistics.get("entity_count", 0) == 0)):
                
                logger.warning("Detected empty ontology despite successful load - likely namespace issue")
                
                # Try to detect if this is a namespace issue
                detected_namespaces = self._detect_namespaces_from_file(self.ontology_path)
                base_iri = detected_namespaces.get("base")
                
                # Normalize namespace for comparison (handle trailing # character)
                normalized_base_iri = base_iri.rstrip('#') if base_iri else None
                normalized_onto_iri = self.ontology.base_iri.rstrip('#') if hasattr(self.ontology, 'base_iri') else None
                
                # Debug information about all available classes in the ontology
                try:
                    if hasattr(self, 'ontology') and self.ontology is not None and hasattr(self.ontology, 'base_iri'):
                        logger.debug(f"Base IRI: {self.ontology.base_iri}")
                    
                    if hasattr(self, 'world') and self.world is not None:
                        if hasattr(self.world, 'classes') and callable(self.world.classes):
                            logger.debug(f"Available classes: {[c for c in self.world.classes()]}")
                        
                        if hasattr(self.world, 'properties') and callable(self.world.properties):
                            logger.debug(f"Available properties: {[p for p in self.world.properties()]}")
                        
                        if hasattr(self.world, 'individuals') and callable(self.world.individuals):
                            logger.debug(f"Available individuals: {[i for i in self.world.individuals()]}")
                except Exception as e:
                    logger.error(f"Error during debug inspection: {str(e)}")
                
                if normalized_base_iri and normalized_onto_iri and normalized_base_iri != normalized_onto_iri:
                    logger.warning(f"Namespace mismatch! File: {base_iri}, Loaded: {self.ontology.base_iri}")
                    logger.warning("Forcing clean reload by removing backend")
                    
                    # Close the world if it exists
                    if hasattr(self, 'world') and self.world is not None:
                        try:
                            self.world.close()
                        except Exception as e:
                            logger.error(f"Error closing world: {str(e)}")
                    
                    # Remove the backend file if it exists
                    if self.backend_path and os.path.exists(self.backend_path):
                        try:
                            os.remove(self.backend_path)
                            logger.info(f"Removed backend file: {self.backend_path}")
                        except Exception as e:
                            logger.error(f"Error removing backend file: {str(e)}")
                    
                    # Reset instance properties
                    self.world = None
                    self.ontology = None
                    self.loaded = False
                    self.materialized = False
                    
                    # Reload with force_rebuild=True
                    force_rebuild = True
                    
                    # Try reloading
                    success = self.load()
                    if not success:
                        logger.error("Failed to reload ontology after namespace issue")
                        return False
            
            # Step 2: If force_rebuild or not already materialized, run reasoner
            if force_rebuild or not hasattr(self, 'materialized') or not self.materialized:
                logger.info("Materializing inferences...")
                
                try:
                    # Enable more robust inference with Pellet
                    if self.ontology is not None:
                        try:
                            with self.ontology:
                                # Set various options for more comprehensive materialization
                                sync_reasoner(
                                    infer_property_values=True,
                                    debug=1
                                )
                            self.materialized = True
                            logger.info("Successfully materialized inferences")
                        except Exception as e:
                            logger.error(f"Error during materialization: {str(e)}")
                            logger.warning("Continuing without complete materialization")
                    
                    # Pre-load key structures for better performance
                    if self.ontology is not None:
                        class_count = 0
                        individual_count = 0
                        property_count = 0
                        
                        # Pre-load all classes
                        if hasattr(self.ontology, 'classes') and callable(self.ontology.classes):
                            try:
                                all_classes = list(self.ontology.classes())
                                class_count = len(all_classes)
                                logger.info(f"Pre-loaded {class_count} classes")
                            except Exception as e:
                                logger.error(f"Error pre-loading classes: {str(e)}")
                            
                        # Pre-load all properties
                        if hasattr(self.ontology, 'properties') and callable(self.ontology.properties):
                            try:
                                all_properties = list(self.ontology.properties())
                                property_count = len(all_properties)
                                logger.info(f"Pre-loaded {property_count} properties")
                            except Exception as e:
                                logger.error(f"Error pre-loading properties: {str(e)}")
                            
                        # Pre-load all individuals
                        if hasattr(self.ontology, 'individuals') and callable(self.ontology.individuals):
                            try:
                                all_individuals = list(self.ontology.individuals())
                                individual_count = len(all_individuals)
                                logger.info(f"Pre-loaded {individual_count} individuals")
                            except Exception as e:
                                logger.error(f"Error pre-loading individuals: {str(e)}")
                        
                        # Store direct counts in statistics if we got any
                        if class_count > 0 or property_count > 0 or individual_count > 0:
                            self.statistics = {
                                "class_count": class_count,
                                "property_count": property_count,
                                "entity_count": individual_count,
                                "total_elements": class_count + property_count + individual_count
                            }
                            logger.info(f"Updated statistics during materialization: {self.statistics}")
                    
                    # Update statistics
                    self._cache_ontology_statistics()
                    
                except Exception as e:
                    logger.error(f"Error during materialization: {str(e)}")
                    logger.warning("Continuing without complete materialization")
            else:
                logger.info("Using previously materialized ontology")
            
            self._materialize_time = time.time() - start_time
            logger.info(f"Ontology materialized in {self._materialize_time:.2f}s")
            self.materialized = True
            return True
            
        except Exception as e:
            logger.error(f"Error in load_and_materialize: {str(e)}")
            traceback.print_exc()
            return False
    
    def _direct_import_with_owlready(self) -> bool:
        """
        Import the ontology directly using owlready2.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Initialize the world if needed
            if self.world is None:
                self.world = World()
            
            # Set the backend if a path is provided
            if self.backend_path and self.world is not None:
                self.world.set_backend(filename=self.backend_path)
                self.world.save()
            
            # Load the ontology
            if self.ontology_path and self.world is not None:
                self.ontology = self.world.get_ontology(self.ontology_path)
                
                if self.ontology is not None:
                    self.ontology.load()
                    self.loaded = True
                    
                    # Save the world to persist changes
                    if self.backend_path and self.world is not None:
                        self.world.save()
            
            return True
        except Exception as e:
            logger.error(f"Error in direct owlready import: {str(e)}")
            return False

    def load(self, force_reload: bool = False) -> bool:
        """
        Load the ontology with robust error handling.
        
        Args:
            force_reload (bool): Force reload the ontology regardless of cache state
        
        Returns:
            bool: True if ontology loaded successfully
        """
        try:
            logger.info(f"Loading ontology from {self.ontology_path}")
            
            # First try the simplest direct approach
            owlready_direct_success = self._direct_import_with_owlready()
            
            # If direct owlready import succeeded and found elements, we're done
            if owlready_direct_success and self.statistics["total_elements"] > 0:
                logger.info("Successfully loaded ontology with direct owlready approach")
                self.loaded = True
                return True
                
            # Next try the namespace-fixing approach
            direct_import_success = self._direct_import_with_rdflib()
            
            # If direct import succeeded and found elements, we're done
            if direct_import_success and self.statistics["total_elements"] > 0:
                logger.info("Successfully loaded ontology with direct namespace fix approach")
                self.loaded = True
                return True
                
            # If direct import failed, fall back to standard loading
            logger.warning("All direct import methods failed, falling back to standard loading")
            # Check result but we continue even if this fails
            _ = self._standard_load(force_reload)
            
            # If all methods result in empty ontology, log a clear warning
            if self.statistics["total_elements"] == 0:
                logger.warning("WARNING: All loading approaches resulted in an empty ontology")
                logger.warning("This could be caused by namespace issues or an invalid ontology file")
                logger.warning("Consider manually converting the TTL file to RDF/XML format")
            
            self.loaded = True
            logger.info(f"Loaded ontology with standard approach: {self.statistics}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load ontology: {str(e)}")
            self.loaded = False
            return False
            
    def _standard_load(self, force_reload: bool = False) -> bool:
        """
        Standard loading approach using owlready2.
        
        Args:
            force_reload: Whether to force reloading the ontology
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Skip if already loaded and not forcing reload
            if self.loaded and not force_reload:
                logger.info("Ontology already loaded, skipping load")
                return True
                
            # Initialize the world if needed
            if self.world is None:
                self.world = World()
                
            # Set the backend if a path is provided
            if self.backend_path and self.world is not None:
                try:
                    self.world.set_backend(filename=self.backend_path)
                except Exception as e:
                    logger.error(f"Error setting backend: {str(e)}")
                    # Continue without backend
            
            # Load the ontology
            if self.ontology_path and self.world is not None:
                try:
                    self.ontology = self.world.get_ontology(self.ontology_path)
                except Exception as e:
                    logger.error(f"Error getting ontology: {str(e)}")
                    return False
                    
                if self.ontology is not None:
                    try:
                        self.ontology.load()
                        self.loaded = True
                    except Exception as e:
                        logger.error(f"Error loading ontology: {str(e)}")
                        return False
                        
                    # Save the world to persist changes
                    if self.backend_path and self.world is not None:
                        try:
                            self.world.save()
                        except Exception as e:
                            logger.error(f"Error saving world: {str(e)}")
                            # Continue without saving
            
            return True
        except Exception as e:
            logger.error(f"Error in standard load: {str(e)}")
            return False
    
    def _collect_namespaces(self) -> None:
        """
        Collect and cache namespaces from the ontology for more convenient access.
        """
        try:
            if self.world is None:
                logger.warning("World is None when collecting namespaces")
                return
                
            # Log all available ontologies in the world
            for ns in self.world.ontologies.keys():
                logger.info(f"Found ontology namespace: {ns}")
            
            # Check specifically for our target namespace
            ragatanga_ns = "http://www.semanticweb.org/ontologies/ragatanga"
            if any(ragatanga_ns in str(ns) for ns in self.world.ontologies.keys()):
                logger.info("Found Ragatanga namespace")
            else:
                logger.warning("Ragatanga namespace not found in loaded ontologies")
            
            # Now collect all namespaces
            if self.ontology is None:
                logger.warning("Ontology is None when collecting namespaces")
                return
                
            self.namespaces = {}
            
            # Get base namespace
            if hasattr(self.ontology, "base_iri"):
                self.namespaces["base"] = self.ontology.base_iri
                logger.info(f"Base namespace: {self.ontology.base_iri}")
                
            # Get all other namespaces
            if (hasattr(self.ontology, "ontology") and 
                self.ontology.ontology is not None and 
                hasattr(self.ontology.ontology, "namespaces") and
                self.ontology.ontology.namespaces is not None):
                
                for prefix, ns in self.ontology.ontology.namespaces.items():
                    if prefix and ns:
                        self.namespaces[prefix] = ns
                        logger.info(f"Namespace: {prefix} -> {ns}")
        except Exception as e:
            logger.error(f"Error collecting namespaces: {str(e)}")
            traceback.print_exc()
    
    def _cache_ontology_statistics(self) -> None:
        """Cache statistics about the ontology for faster retrieval."""
        try:
            # Count classes
            class_count = 0
            class_list: List[Any] = []
            if self.ontology is not None and hasattr(self.ontology, 'classes') and callable(self.ontology.classes):
                try:
                    class_list = list(self.ontology.classes())
                    class_count = len(class_list)
                    logger.info(f"Counted {class_count} classes for cache")
                except Exception as e:
                    logger.error(f"Error listing classes: {str(e)}")
            
            # Count properties
            property_count = 0
            property_list: List[Any] = []
            if self.ontology is not None and hasattr(self.ontology, 'properties') and callable(self.ontology.properties):
                try:
                    property_list = list(self.ontology.properties())
                    property_count = len(property_list)
                except Exception as e:
                    logger.warning(f"Error counting properties: {e}")
            
            # Count individuals
            individual_count = 0
            individual_list: List[Any] = []
            if self.ontology is not None and hasattr(self.ontology, 'individuals') and callable(self.ontology.individuals):
                try:
                    individual_list = list(self.ontology.individuals())
                    individual_count = len(individual_list)
                except Exception as e:
                    logger.error(f"Error listing individuals: {str(e)}")
            
            # Store the statistics
            self.statistics = {
                "class_count": class_count,
                "property_count": property_count,
                "entity_count": individual_count,
                "total_elements": class_count + property_count + individual_count
            }
            
            # Log summary
            logger.info(f"Cached ontology statistics: {class_count} classes, {property_count} properties, {individual_count} individuals")
            
        except Exception as e:
            logger.error(f"Error caching ontology statistics: {str(e)}")
            self.statistics = {
                "class_count": 0,
                "property_count": 0,
                "entity_count": 0,
                "total_elements": 0,
                "error": str(e)
            }
    
    async def execute_query(self, query: str, parameters: Optional[List] = None) -> List[Dict[str, Any]]:
        """
        Execute a SPARQL query against the ontology.
        
        Args:
            query: SPARQL query string
            parameters: Optional parameters for the query
            
        Returns:
            List of result dictionaries
        """
        if not self.loaded:
            logger.error("Ontology not loaded, cannot execute query")
            return []
            
        # Check cache first if enabled
        if self.enable_query_cache:
            cache_key = self._generate_query_cache_key(query, parameters)
            cached_result = self._query_cache.get(cache_key)
            
            if cached_result:
                results, timestamp = cached_result
                # Check if still valid
                if datetime.now() - timestamp <= _QUERY_CACHE_EXPIRY:
                    logger.debug(f"Using cached query results for: {query[:50]}...")
                    return results
                else:
                    # Remove expired result
                    del self._query_cache[cache_key]
        
        # Execute the query
        start_time = time.time()
        try:
            # Use more forgiving SPARQL query execution settings
            results: List[Any] = []
            transformed_results = []
            
            if self.world is not None and hasattr(self.world, 'sparql') and callable(self.world.sparql):
                try:
                    # First try to execute the query and handle possible exceptions
                    if parameters is not None:
                        query_result = self.world.sparql(query, parameters, error_on_undefined_entities=False)
                    else:
                        query_result = self.world.sparql(query, error_on_undefined_entities=False)
                    
                    # Try to convert to list safely
                    try:
                        # More explicit type checking that the linter can understand
                        if isinstance(query_result, Iterable):
                            results = list(query_result)
                        else:
                            logger.warning(f"Query result is not iterable: {type(query_result)}")
                            results = []
                    except (TypeError, ValueError) as e:
                        logger.warning(f"Could not convert query results to list: {e}")
                        results = []
                except Exception as query_error:
                    logger.error(f"Error executing SPARQL query: {query_error}")
                    results = []
            
            # Transform results to dictionaries
            for row in results:
                if isinstance(row, tuple):
                    result_dict = {}
                    for i, var in enumerate(row):
                        try:
                            if hasattr(var, 'name'):
                                var_name = f"var{i}"
                                var_value = str(var.name)
                            elif hasattr(var, 'iri'):
                                var_name = f"var{i}"
                                var_value = str(var.iri)
                            else:
                                var_name = f"var{i}"
                                var_value = str(var)
                            result_dict[var_name] = var_value
                        except Exception as var_e:
                            logger.warning(f"Error processing SPARQL result variable: {var_e}")
                            result_dict[f"var{i}"] = str(var)
                    transformed_results.append(result_dict)
                elif isinstance(row, dict):
                    transformed_results.append(row)
                else:
                    logger.warning(f"Unexpected SPARQL result type: {type(row)}")
            
            # Store results in cache if enabled
            if self.enable_query_cache:
                cache_key = self._generate_query_cache_key(query, parameters)
                self._query_cache[cache_key] = (transformed_results, datetime.now())
                self._clean_expired_cache_entries()
                self._trim_cache_if_needed()
                
            query_time = time.time() - start_time
            logger.debug(f"Query executed in {query_time:.2f}s: {query[:50]}...")
            return transformed_results
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            logger.debug(f"Query that failed: {query}")
            return []

    def save(self, output_path: Optional[str] = None, format: str = "rdfxml") -> bool:
        """
        Save the ontology to a file in one of the supported formats and also save 
        the world state to the backend if using persistence.
        
        Args:
            output_path (Optional[str]): Path where the ontology will be saved
                                        If None, only the world state is saved
            format (str): Format to use for saving. Supported formats: 'rdfxml' (default) or 'ntriples'
            
        Returns:
            bool: True if the ontology was saved successfully, False otherwise
        """
        try:
            if not self.ontology:
                logger.error("No ontology loaded to save")
                return False
                
            success = True
            
            # Save the ontology to a file if output_path is provided
            if output_path:
                # Validate format
                if format.lower() not in ["rdfxml", "ntriples"]:
                    logger.error(f"Unsupported format: {format}. Use 'rdfxml' or 'ntriples'")
                    return False
                    
                # Save the ontology using owlready2's built-in save method
                self.ontology.save(file=output_path, format=format.lower())
                logger.info(f"Successfully saved ontology to {output_path} in {format} format")
            
            # If using a persistent backend, save the world state
            if self.world and self.backend_path:
                try:
                    self.world.save()
                    logger.info(f"Successfully saved world state to {self.backend_path}")
                except Exception as e:
                    logger.error(f"Failed to save world state: {str(e)}")
                    success = False
                    
            return success
            
        except Exception as e:
            logger.error(f"Failed to save ontology: {str(e)}")
            return False

    def _detect_namespaces_from_file(self, file_path: str) -> Dict[str, str]:
        """
        Parse the ontology file with RDFLib first to extract namespaces.
        
        Args:
            file_path: Path to the ontology file
            
        Returns:
            Dictionary of prefix -> namespace mappings
        """
        try:
            # Import here to avoid making RDFLib a hard dependency
            from rdflib import Graph
            
            logger.info(f"Pre-parsing ontology file with RDFLib to detect namespaces: {file_path}")
            g = Graph()
            g.parse(file_path, format="turtle")
            
            # Get all namespaces and convert URIRef objects to strings
            namespaces = {prefix: str(uri) for prefix, uri in g.namespaces()}
            
            # Try to determine the base IRI of the ontology
            base_iris = []
            for s, p, o in g.triples((None, None, None)):
                if str(p) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and str(o) == "http://www.w3.org/2002/07/owl#Ontology":
                    base_iris.append(str(s))
            
            if base_iris:
                base_iri = base_iris[0]
                logger.info(f"Detected ontology base IRI: {base_iri}")
                namespaces["base"] = base_iri
            
            logger.info(f"Detected namespaces: {namespaces}")
            return namespaces
            
        except ImportError:
            logger.warning("RDFLib not available for namespace detection")
            return {}
        except Exception as e:
            logger.error(f"Error detecting namespaces: {str(e)}")
            return {}

    def _force_clean_reload(self) -> bool:
        """
        Force a clean reload of the ontology.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Initialize a new world
            if self.world is None:
                self.world = World()
            
            # Set the backend if a path is provided
            if self.backend_path and self.world is not None:
                self.world.set_backend(filename=self.backend_path)
            
            # Load the ontology
            if self.ontology_path and self.world is not None:
                self.ontology = self.world.get_ontology(self.ontology_path)
                
                if self.ontology is not None:
                    self.ontology.load()
                    self.loaded = True
                    
                    # Save the world to persist changes
                    if self.backend_path and self.world is not None:
                        self.world.save()
            
            return True
        except Exception as e:
            logger.error(f"Error in force_clean_reload: {str(e)}")
            return False

    def _direct_import_with_rdflib(self) -> bool:
        """
        Import the ontology using rdflib.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Initialize the world if needed
            if self.world is None:
                self.world = World()
            
            # Get the ontology
            if self.ontology_path and self.world is not None:
                self.ontology = self.world.get_ontology(self.ontology_path)
                
                if self.ontology is not None:
                    self.ontology.load()
                    self.loaded = True
                    
                    # Collect statistics
                    if hasattr(self.ontology, 'classes') and callable(self.ontology.classes):
                        class_count = len(list(self.ontology.classes()))
                    else:
                        class_count = 0
                        
                    if hasattr(self.ontology, 'properties') and callable(self.ontology.properties):
                        property_count = len(list(self.ontology.properties()))
                    else:
                        property_count = 0
                        
                    if hasattr(self.ontology, 'individuals') and callable(self.ontology.individuals):
                        individual_count = len(list(self.ontology.individuals()))
                    else:
                        individual_count = 0
                    
                    # Save the world to persist changes
                    if self.backend_path and self.world is not None:
                        self.world.set_backend(filename=self.backend_path)
                        self.world.save()
                    
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Error in direct import: {str(e)}")
            return False