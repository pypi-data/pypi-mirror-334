from typing import List, Dict, Any
import logging
import traceback

logger = logging.getLogger(__name__)

class AdaptiveRetriever:
    def __init__(self, ontology_manager=None):
        """
        Initialize the AdaptiveRetriever with an optional ontology manager.
        
        Args:
            ontology_manager: The ontology manager to use for SPARQL queries
        """
        self.ontology_manager = ontology_manager
        
    async def _execute_sparql_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a SPARQL query against the ontology.
        
        Args:
            query: SPARQL query to execute
            
        Returns:
            List of result dictionaries
        """
        logger.debug(f"Executing SPARQL query: {query}")
        
        if not self.ontology_manager:
            logger.error("OntologyManager not initialized, cannot execute SPARQL query")
            return []
            
        try:
            results = await self.ontology_manager.execute_sparql(query)
            
            # Convert results to dictionary format if they're not already
            if results and isinstance(results, list):
                if results and isinstance(results[0], str):
                    # Handle legacy string results format
                    logger.debug("Converting legacy string results to dictionary format")
                    return [{"result": result} for result in results if result]
                elif results and isinstance(results[0], dict):
                    # Already in dictionary format
                    return results
                else:
                    # Unknown format
                    logger.warning(f"Unknown result format from execute_sparql: {type(results[0])}")
                    return []
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error executing SPARQL query: {str(e)}")
            logger.error(traceback.format_exc())
            return [] 