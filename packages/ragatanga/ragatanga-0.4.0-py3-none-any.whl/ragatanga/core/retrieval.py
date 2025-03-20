"""
Hybrid retrieval module for Ragatanga.

This module implements a hybrid retrieval approach combining ontology-based and
semantic search retrieval with adaptive parameter tuning.
"""

import re
import json
import time
from collections import OrderedDict
from typing import Any, List, Optional, Tuple, Dict

from loguru import logger

from ragatanga.core.query import analyze_query_type
from ragatanga.utils.sparql import generate_sparql_query
from ragatanga.utils.text import text_similarity
from ragatanga.core.models import RetrievalResult
from ragatanga.core.owl_retriever import UniversalOntologyManager
from ragatanga.core.semantic import SemanticSearch
from ragatanga.schemas.retrieval import RetrievalConfig


class LRUCache(OrderedDict):
    """Simple LRU cache implementation based on OrderedDict."""

    def __init__(self, max_size: int = 100):
        """
        Initialize LRU cache.

        Args:
            max_size: Maximum number of items to store in the cache.
        """
        super().__init__()
        self.max_size = max_size

    def __getitem__(self, key: str) -> Any:
        """Retrieve item and update its position in the order."""
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        """Insert item and maintain maximum cache size."""
        super().__setitem__(key, value)
        if len(self) > self.max_size:
            oldest = next(iter(self))
            del self[oldest]


class AdaptiveRetriever:
    """
    Adaptive retriever that combines ontology-based and semantic search.
    
    This class provides a unified interface for retrieving information using
    both ontology-based reasoning and semantic search, adaptively weighting
    the results based on confidence scores.
    """
    
    def __init__(
        self,
        ontology_manager: UniversalOntologyManager,
        semantic_provider: Optional[SemanticSearch] = None,
        config: Optional[RetrievalConfig] = None,
    ):
        """
        Initialize the adaptive retriever.
        
        Args:
            ontology_manager: The ontology manager to use for ontology-based retrieval
            semantic_provider: Optional semantic search provider
            config: Optional retrieval configuration
        """
        self.ontology_manager = ontology_manager
        self.semantic_provider = semantic_provider or SemanticSearch()
        self.config = config or RetrievalConfig()
        
        # Performance metrics
        self._last_query_time = 0.0
        self._ontology_query_time = 0.0
        self._semantic_query_time = 0.0
        
        # Simple LRU cache to store calculated parameters for similar queries
        self.query_cache = LRUCache(max_size=100)

    async def retrieve(
        self, 
        query: str, 
        max_results: int = 5,
        confidence_threshold: float = 0.0,
        parameters: Optional[List] = None,
    ) -> List[RetrievalResult]:
        """
        Retrieve information using both ontology and semantic search.
        
        Args:
            query: The query string
            max_results: Maximum number of results to return
            confidence_threshold: Minimum confidence score for results
            parameters: Optional parameters for the query
            
        Returns:
            List of retrieval results
        """
        start_time = time.time()
        
        # Run ontology and semantic search in parallel
        ontology_results = await self._retrieve_from_ontology(query, parameters)
        semantic_results = await self._retrieve_from_semantic(query)
        
        # Combine and rank results
        combined_results = self._combine_results(
            ontology_results, 
            semantic_results,
            max_results,
            confidence_threshold
        )
        
        self._last_query_time = time.time() - start_time
        logger.debug(f"Total retrieval time: {self._last_query_time:.2f}s")
        
        return combined_results
        
    async def batch_retrieve(
        self,
        queries: List[str],
        max_results_per_query: int = 5,
        confidence_threshold: float = 0.0,
        parameters: Optional[List] = None,
    ) -> List[List[RetrievalResult]]:
        """
        Retrieve information for multiple queries in batch.
        
        Args:
            queries: List of query strings
            max_results_per_query: Maximum results per query
            confidence_threshold: Minimum confidence score for results
            parameters: Optional parameters for the queries
            
        Returns:
            List of retrieval results for each query
        """
        start_time = time.time()
        
        # Process semantic search in batch (more efficient)
        semantic_batch_results = await self._batch_semantic_search(queries)
        
        # Process ontology queries (could be parallelized further if needed)
        results = []
        for i, query in enumerate(queries):
            # Get the semantic results for this query
            semantic_results = semantic_batch_results[i]
            
            # Get ontology results
            ontology_results = await self._retrieve_from_ontology(query, parameters)
            
            # Combine and rank
            combined = self._combine_results(
                ontology_results,
                semantic_results,
                max_results_per_query,
                confidence_threshold
            )
            
            results.append(combined)
            
        batch_time = time.time() - start_time
        logger.debug(f"Batch retrieval for {len(queries)} queries completed in {batch_time:.2f}s")
        
        return results
    
    async def _batch_semantic_search(self, queries: List[str]) -> List[List[RetrievalResult]]:
        """
        Perform semantic search for multiple queries in batch.
        
        Args:
            queries: List of query strings
            
        Returns:
            List of semantic search results for each query
        """
        if not self.semantic_provider or not queries:
            return [[] for _ in queries]
            
        try:
            # Use the semantic provider's batch search if available
            if hasattr(self.semantic_provider, 'batch_search'):
                string_batch_results = await self.semantic_provider.batch_search(
                    queries,
                    k=self.config.max_semantic_results
                )
                
                # Convert string results to RetrievalResult objects
                batch_results = []
                for query_idx, query_results in enumerate(string_batch_results):
                    query = queries[query_idx]
                    results = []
                    for i, content in enumerate(query_results):
                        result = RetrievalResult(
                            content=content,
                            metadata={
                                "source": "semantic",
                                "query": query,
                                "rank": i + 1,
                            },
                            confidence=1.0 - (i * 0.05)  # Decrease confidence slightly for lower ranks
                        )
                        results.append(result)
                    batch_results.append(results)
                return batch_results
            
            # Fall back to individual searches
            results = []
            for query in queries:
                query_results = await self._retrieve_from_semantic(query)
                results.append(query_results)
                
            return results
            
        except Exception as e:
            logger.error(f"Error in batch semantic search: {str(e)}")
            return [[] for _ in queries]
    
    async def _retrieve_from_ontology(
        self, 
        query: str,
        parameters: Optional[List] = None,
    ) -> List[RetrievalResult]:
        """
        Retrieve information from the ontology.
        
        Args:
            query: The query string
            parameters: Optional parameters for the query
            
        Returns:
            List of retrieval results from the ontology
        """
        if not self.ontology_manager:
            return []
            
        ontology_start = time.time()
        try:
            # Generate SPARQL query
            schema = self.ontology_manager.get_ontology_structure()
            sparql_query = await generate_sparql_query(
                query, 
                json.dumps(schema, indent=2), 
                parameters=parameters
            )
            
            # Execute the query
            query_results = await self.ontology_manager.execute_query(sparql_query, parameters)
            
            # Convert to RetrievalResult objects
            results = []
            for item in query_results:
                # Process each result
                result = RetrievalResult(
                    content=json.dumps(item, indent=2),
                    metadata={
                        "source": "ontology",
                        "query": query,
                        "sparql_query": sparql_query,
                    },
                    confidence=self.config.ontology_confidence
                )
                results.append(result)
                
            self._ontology_query_time = time.time() - ontology_start
            logger.debug(f"Ontology retrieval time: {self._ontology_query_time:.2f}s")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in ontology retrieval: {str(e)}")
            self._ontology_query_time = time.time() - ontology_start
            return []
            
    async def _retrieve_from_semantic(self, query: str) -> List[RetrievalResult]:
        """
        Retrieve information using semantic search.
        
        Args:
            query: The query string
            
        Returns:
            List of retrieval results from semantic search
        """
        if not self.semantic_provider:
            return []
            
        semantic_start = time.time()
        try:
            # Get string results from semantic search
            string_results = await self.semantic_provider.search(
                query,
                k=self.config.max_semantic_results
            )
            
            # Convert to RetrievalResult objects
            results = []
            for i, content in enumerate(string_results):
                result = RetrievalResult(
                    content=content,
                    metadata={
                        "source": "semantic",
                        "query": query,
                        "rank": i + 1,
                    },
                    confidence=1.0 - (i * 0.05)  # Decrease confidence slightly for lower ranks
                )
                results.append(result)
            
            self._semantic_query_time = time.time() - semantic_start
            logger.debug(f"Semantic retrieval time: {self._semantic_query_time:.2f}s")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in semantic retrieval: {str(e)}")
            self._semantic_query_time = time.time() - semantic_start
            return []
            
    def _combine_results(
        self,
        ontology_results: List[RetrievalResult],
        semantic_results: List[RetrievalResult],
        max_results: int,
        confidence_threshold: float,
    ) -> List[RetrievalResult]:
        """
        Combine and rank results from ontology and semantic search.
        
        Args:
            ontology_results: Results from ontology search
            semantic_results: Results from semantic search
            max_results: Maximum number of results to return
            confidence_threshold: Minimum confidence score
            
        Returns:
            Combined and ranked list of results
        """
        # Apply weights from config
        for result in ontology_results:
            result.confidence *= self.config.ontology_weight
            
        for result in semantic_results:
            result.confidence *= self.config.semantic_search_weight
            
        # Combine results
        combined = ontology_results + semantic_results
        
        # Filter by confidence threshold
        if confidence_threshold > 0:
            combined = [r for r in combined if r.confidence >= confidence_threshold]
            
        # Sort by confidence (descending)
        combined.sort(key=lambda x: x.confidence, reverse=True)
        
        # Limit to max results
        return combined[:max_results]
        
    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Get performance metrics for the last retrieval operation.
        
        Returns:
            Dictionary of performance metrics
        """
        return {
            "total_time": self._last_query_time,
            "ontology_time": self._ontology_query_time,
            "semantic_time": self._semantic_query_time,
        }

    async def _analyze_and_calculate_parameters(
        self, query: str
    ) -> Tuple[float, float, int]:
        """
        Analyze the query and compute the appropriate retrieval parameters.

        Args:
            query: The query string to analyze.

        Returns:
            Tuple of (sparql_weight, semantic_weight, top_k).
        """
        query_complexity = await self._analyze_query_complexity(query)
        query_specificity = await self._analyze_query_specificity(query)
        query_type = await analyze_query_type(query)

        return self._calculate_parameters(query_complexity, query_specificity, query_type)

    async def _analyze_query_complexity(self, query: str) -> float:
        """
        Analyze the complexity of the query on a scale from 0 (simple) to 1 (complex).

        Consider:
          - Query length.
          - Presence of complex-indicator words.
          - Number of potential entities in the query.

        Args:
            query: The query string.

        Returns:
            A float representing the complexity score.
        """
        words = query.split()
        # Longer queries can be considered more complex (capped at 1.0)
        length_factor = min(len(words) / 20.0, 1.0)

        # Track if the query includes words often used in comparisons or relationships
        complex_indicators = ["compare", "difference", "versus", "relationship", "between"]
        structure_factor = 0.5 * sum(
            any(ind in word.lower() for ind in complex_indicators)
            for word in words
        ) / len(words) if words else 0.0

        potential_entities = await self._get_potential_entities(query)
        entity_factor = min(len(potential_entities) / 3.0, 1.0)

        complexity = (0.4 * length_factor) + (0.3 * structure_factor) + (0.3 * entity_factor)
        return min(complexity, 1.0)

    async def _analyze_query_specificity(self, query: str) -> float:
        """
        Analyze how specific the query is to ontology entities, on a scale from 0 to 1.

        Consider:
          - Ratio of identified potential entities that match actual ontology entities.
          - Presence of domain-specific keywords.

        Args:
            query: The query string.

        Returns:
            A float representing the specificity score (0 to 1).
        """
        potential_entities = await self._get_potential_entities(query)
        if not potential_entities:
            return 0.3

        matched_entities = await self._match_entities_in_ontology(potential_entities)
        match_ratio = len(matched_entities) / len(potential_entities) if potential_entities else 0.0

        # Example domain-specific keywords
        specificity_keywords = ["unidade", "plano", "modalidade", "benefício", "piscina", "tipo"]
        keyword_factor = sum(0.2 for kw in specificity_keywords if kw in query.lower())

        specificity = (0.6 * match_ratio) + (0.4 * min(keyword_factor, 1.0))
        return min(specificity, 1.0)

    def _calculate_parameters(
        self, complexity: float, specificity: float, query_type: str
    ) -> Tuple[float, float, int]:
        """
        Derive weights (for SPARQL and semantic search) and top_k based on
        query complexity, specificity, and type.

        Args:
            complexity: Complexity score (0 to 1).
            specificity: Specificity score (0 to 1).
            query_type: The query type (e.g., 'factual', 'descriptive', etc.).

        Returns:
            A tuple (sparql_weight, semantic_weight, top_k).
        """
        # Base weights influenced by specificity
        sparql_weight = self.config.ontology_weight + 0.3 * specificity
        semantic_weight = self.config.semantic_search_weight + 0.2 * (1 - specificity)

        # Adjust top_k by complexity factor
        top_k = int(self.config.max_results * (1 + complexity))

        # Fine-tune based on query type
        if query_type == "factual":
            sparql_weight += 0.1
        elif query_type == "descriptive":
            semantic_weight += 0.1
        elif query_type == "comparative":
            top_k += 5
        elif query_type == "exploratory":
            top_k += 10

        # Keep values within defined bounds
        sparql_weight = min(max(sparql_weight, 0.3), 1.0)
        semantic_weight = min(max(semantic_weight, 0.3), 1.0)
        top_k = min(max(top_k, self.config.min_results), self.config.max_results)

        return sparql_weight, semantic_weight, top_k

    async def _perform_combined_retrieval(
        self, query: str, sparql_weight: float, semantic_weight: float, top_k: int, 
        parameters: Optional[List] = None
    ) -> Tuple[List[RetrievalResult], List[float]]:
        """
        Perform retrieval using both SPARQL and semantic search methods.

        Args:
            query: The natural language query string.
            sparql_weight: The weight to assign to SPARQL results (0.0-1.0).
            semantic_weight: The weight to assign to semantic search results (0.0-1.0).
            top_k: The number of semantic search results to retrieve.
            parameters: Optional parameters for parameterized SPARQL queries.

        Returns:
            A tuple of (merged_results, confidence_scores).
        """
        # Perform both retrievals in parallel
        ontology_results = await self._retrieve_from_ontology(query, parameters)
        semantic_results = await self._retrieve_from_semantic(query)

        # Merge and deduplicate results
        merged_results, confidence_scores = self._merge_and_deduplicate_results(
            ontology_results,
            semantic_results,
            sparql_weight,
            semantic_weight
        )

        return merged_results, confidence_scores

    def _merge_and_deduplicate_results(
        self,
        ontology_results: List[RetrievalResult],
        semantic_results: List[RetrievalResult],
        sparql_weight: float,
        semantic_weight: float
    ) -> Tuple[List[RetrievalResult], List[float]]:
        """
        Merge SPARQL and semantic results with weighted scores.
        NOTE: Deduplication is currently disabled for troubleshooting purposes.

        Args:
            ontology_results: List of SPARQL results.
            semantic_results: List of semantic results.
            sparql_weight: Weight factor for SPARQL results.
            semantic_weight: Weight factor for semantic results.

        Returns:
            A tuple (merged_results, confidence_scores) with all results.
        """
        merged_results = []
        confidence_scores = []

        # Incorporate SPARQL results
        for idx, result in enumerate(ontology_results):
            # Skip error or empty placeholders
            if (
                isinstance(result, RetrievalResult)
                and ("error" in result.content.lower() or "no matching results" in result.content.lower())
            ):
                continue
            # Position-based weight factor
            pos_weight = self._compute_result_position_weight(idx, len(ontology_results))
            final_weight = sparql_weight * pos_weight

            merged_results.append(result)
            confidence_scores.append(final_weight)

        # Incorporate semantic results
        for idx, result in enumerate(semantic_results):
            pos_weight = self._compute_result_position_weight(idx, len(semantic_results))
            final_weight = semantic_weight * pos_weight

            merged_results.append(result)
            confidence_scores.append(final_weight)

        # Sort by confidence score (descending)
        sorted_pairs = sorted(
            zip(confidence_scores, merged_results),
            key=lambda pair: pair[0],
            reverse=True
        )
        sorted_scores, sorted_results = zip(*sorted_pairs) if sorted_pairs else ([], [])

        # DEDUPLICATION DISABLED - Return all results sorted by score
        return list(sorted_results), list(sorted_scores)

    def _compute_result_position_weight(self, index: int, total: int) -> float:
        """
        Compute a position-based weight factor that slightly discounts lower-ranked results.

        Args:
            index: Zero-based rank of the result.
            total: Total number of results.

        Returns:
            A float factor between 0.5 and 1.0, inclusive.
        """
        if total <= 1:
            return 1.0
        return 1.0 - (index / (total - 1)) * 0.5

    def _deduplicate_by_similarity(
        self, results: List[RetrievalResult], scores: List[float]
    ) -> Tuple[List[RetrievalResult], List[float]]:
        """
        Remove near-duplicate results by checking textual similarity.
        Currently not in use - deduplication disabled.

        Args:
            results: Ordered list of results.
            scores: Corresponding list of confidence scores.

        Returns:
            (unique_results, unique_scores) with duplicates removed.
        """
        unique_results: List[RetrievalResult] = []
        unique_scores: List[float] = []

        for i, result in enumerate(results):
            # Extract the actual text portion to compare
            result_text = self._extract_result_text(result)

            # Skip result if it's too similar to any previously added
            if any(
                text_similarity(result_text, self._extract_result_text(prev)) > self.config.similarity_threshold
                for prev in unique_results
            ):
                continue

            unique_results.append(result)
            unique_scores.append(scores[i])

        return unique_results, unique_scores

    @staticmethod
    def _extract_result_text(result: RetrievalResult) -> str:
        """
        Strip the leading prefix (e.g. 'SPARQL: ' or 'Semantic: ') to isolate
        the actual result content.

        Args:
            result: The full result string, including prefix.

        Returns:
            The result text without the prefix.
        """
        return result.content.split(":", 1)[1].strip() if ":" in result.content else result.content

    async def _get_potential_entities(self, query: str) -> List[str]:
        """
        Identify potential entity mentions in the query.

        Uses capitalization, adjacent capitalized words, and quoted phrases.

        Args:
            query: The user's query.

        Returns:
            A list of potential entities (strings).
        """
        words = query.split()
        potential_entities = set()

        # Single capitalized words
        for word in words:
            if word and word[0].isupper():
                potential_entities.add(word)

        # Adjacent capitalized words (to form multi-word entities)
        for i in range(len(words) - 1):
            if words[i] and words[i][0].isupper() and words[i + 1][0].isupper():
                potential_entities.add(f"{words[i]} {words[i + 1]}")

        # Quoted phrases
        quoted_phrases = re.findall(r'"([^"]*)"', query)
        potential_entities.update(quoted_phrases)

        return list(potential_entities)

    async def _match_entities_in_ontology(self, potential_entities: List[str]) -> List[str]:
        """
        Match potential entities against the ontology.

        Args:
            potential_entities: A list of possible entity strings.

        Returns:
            A list of entities that were matched in the ontology.
        """
        if not self.ontology_manager:
            return []

        matched_entities = []
        all_labels = set()

        # Get ontology structure which contains classes and properties
        structure = self.ontology_manager.get_ontology_structure()
        
        # Extract labels from classes
        for cls in structure.get("classes", []):
            if "label" in cls and cls["label"]:
                all_labels.add(str(cls["label"]).lower())
            if "entity" in cls and isinstance(cls["entity"], dict) and "id" in cls["entity"]:
                all_labels.add(cls["entity"]["id"].lower())

        # Extract labels from properties
        for prop in structure.get("properties", []):
            if "label" in prop and prop["label"]:
                all_labels.add(str(prop["label"]).lower())
            if "prop" in prop and isinstance(prop["prop"], dict) and "id" in prop["prop"]:
                all_labels.add(prop["prop"]["id"].lower())
                
        # Query for additional labels if we don't have enough
        if len(all_labels) < 10:
            try:
                query = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?label 
                WHERE { 
                   ?s rdfs:label ?label 
                }
                LIMIT 100
                """
                results = await self.ontology_manager.execute_query(query)
                for result in results:
                    if "label" in result:
                        all_labels.add(str(result["label"]).lower())
            except Exception as e:
                logger.error(f"Error querying for labels: {str(e)}")

        # Check if potential entity is in the set of known labels
        for entity in potential_entities:
            entity_lower = entity.lower()
            if any(entity_lower in label or label in entity_lower for label in all_labels):
                matched_entities.append(entity)

        return matched_entities

    def _get_cached_parameters(self, query: str) -> Tuple[bool, Tuple[float, float, int]]:
        """
        Retrieve parameters from cache if an exact or near-exact query is found.

        Args:
            query: The query string.

        Returns:
            (cache_hit, (sparql_weight, semantic_weight, top_k)).
        """
        # Exact match
        if query in self.query_cache:
            return True, self.query_cache[query]

        # Check for near-duplicates
        for cached_query, params in self.query_cache.items():
            if text_similarity(query, cached_query) > self.config.similarity_threshold:
                return True, params

        # No match found
        default_params = (self.config.ontology_weight, self.config.semantic_search_weight, self.config.max_results)
        return False, default_params

    def _store_in_cache(self, query: str, parameters: Tuple[float, float, int]) -> None:
        """
        Store computed retrieval parameters for the given query in the cache.

        Args:
            query: The query string.
            parameters: (sparql_weight, semantic_weight, top_k).
        """
        self.query_cache[query] = parameters