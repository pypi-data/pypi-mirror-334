"""
SPARQL endpoint implementation for Ragatanga.

This module provides a W3C-compliant SPARQL endpoint using owlready2's endpoint functionality.
It follows the SPARQL 1.1 Protocol recommendation:
https://www.w3.org/TR/sparql11-protocol/
"""

from typing import Optional, Any
import logging
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from starlette.responses import JSONResponse, PlainTextResponse

from ragatanga.core.owl_retriever import UniversalOntologyManager
from ragatanga.api.dependencies import get_tenant_id, get_tenant_ontology_manager
from ragatanga.utils.sparql import validate_sparql_query

logger = logging.getLogger(__name__)

# Create a router for the standard SPARQL endpoint
sparql_router = APIRouter(prefix="/standard-sparql", tags=["SPARQL"])


class FastAPIEndPoint:
    """
    SPARQL endpoint implementation for FastAPI using owlready2.
    
    This implementation is optimized for owlready2's native SPARQL engine.
    """
    
    def __init__(self, world):
        """Initialize with an owlready2 world."""
        self.world = world
    
    def handle_query(self, query: str, accept_header: str) -> Response:
        """
        Handle a SPARQL query and format the response based on accept header.
        
        Args:
            query: The SPARQL query string
            accept_header: The HTTP Accept header value
            
        Returns:
            A FastAPI Response object with appropriate content
        """
        try:
            # Validate the query
            is_valid, error_message = validate_sparql_query(query)
            if not is_valid:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid SPARQL query", "details": error_message}
                )
            
            # Execute the query
            if "application/sparql-results+json" in accept_header:
                result_format = "json"
            elif "application/sparql-results+xml" in accept_header:
                result_format = "xml"
            else:
                result_format = "json"  # Default
            
            # Process the results
            results = self._execute_query(query, result_format)
            
            # Return appropriate response based on format
            if result_format == "json":
                return JSONResponse(content=results)
            else:
                return PlainTextResponse(content=results)
                
        except Exception as e:
            logger.error(f"Error handling SPARQL query: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"error": "Error executing SPARQL query", "details": str(e)}
            )
    
    def _execute_query(self, query: str, result_format: str) -> Any:
        """
        Execute a SPARQL query and format the results.
        
        Args:
            query: The SPARQL query string
            result_format: The desired result format ('json' or 'xml')
            
        Returns:
            Formatted query results
        """
        # Execute the query
        raw_results = list(self.world.sparql(query, error_on_undefined_entities=False))
        
        # For SELECT queries - format the results
        if query.upper().strip().startswith("SELECT"):
            return self._format_select_results(raw_results, result_format)
        # For INSERT/DELETE queries - return success message
        elif query.upper().strip().startswith("INSERT") or query.upper().strip().startswith("DELETE"):
            if isinstance(raw_results, int):
                # Return number of triples modified
                return {
                    "success": True,
                    "modified": raw_results,
                    "message": f"Query executed successfully. {raw_results} triple(s) modified."
                }
            else:
                return {
                    "success": True,
                    "message": "Query executed successfully."
                }
        else:
            # For other query types
            return {
                "success": True,
                "results": str(raw_results),
                "message": "Query executed successfully."
            }
    
    def _format_select_results(self, results, result_format: str) -> Any:
        """Format SELECT query results in the specified format."""
        if not results:
            if result_format == "json":
                return {
                    "head": {"vars": []},
                    "results": {"bindings": []}
                }
            else:
                return '<?xml version="1.0"?>\n<sparql xmlns="http://www.w3.org/2005/sparql-results#">\n<head></head>\n<results></results>\n</sparql>'
        
        if result_format == "json":
            # Convert to SPARQL JSON results format
            bindings = []
            
            # Determine variable names
            var_names = []
            if hasattr(results[0], "__len__") and len(results[0]) > 0:
                var_names = [f"var{i}" for i in range(len(results[0]))]
            
            for row in results:
                binding = {}
                if isinstance(row, tuple):
                    for i, value in enumerate(row):
                        var_name = var_names[i] if i < len(var_names) else f"var{i}"
                        
                        if hasattr(value, "iri"):
                            binding[var_name] = {"type": "uri", "value": str(value.iri)}
                        elif hasattr(value, "name"):
                            binding[var_name] = {"type": "literal", "value": str(value.name)}
                        else:
                            binding[var_name] = {"type": "literal", "value": str(value)}
                    bindings.append(binding)
                elif row is not None:
                    # Handle single value result
                    binding[var_names[0] if var_names else "var0"] = {"type": "literal", "value": str(row)}
                    bindings.append(binding)
            
            return {
                "head": {"vars": var_names},
                "results": {"bindings": bindings}
            }
        else:
            # Return XML format
            xml_output = '<?xml version="1.0"?>\n'
            xml_output += '<sparql xmlns="http://www.w3.org/2005/sparql-results#">\n'
            xml_output += '  <head>\n'
            
            # Determine variable names
            var_names = []
            if hasattr(results[0], "__len__") and len(results[0]) > 0:
                var_names = [f"var{i}" for i in range(len(results[0]))]
                for name in var_names:
                    xml_output += f'    <variable name="{name}"/>\n'
            
            xml_output += '  </head>\n'
            xml_output += '  <results>\n'
            
            for row in results:
                xml_output += '    <result>\n'
                if isinstance(row, tuple):
                    for i, value in enumerate(row):
                        var_name = var_names[i] if i < len(var_names) else f"var{i}"
                        xml_output += f'      <binding name="{var_name}">\n'
                        
                        if hasattr(value, "iri"):
                            xml_output += f'        <uri>{str(value.iri)}</uri>\n'
                        else:
                            xml_output += f'        <literal>{str(value)}</literal>\n'
                        
                        xml_output += '      </binding>\n'
                elif row is not None:
                    # Handle single value result
                    var_name = var_names[0] if var_names else "var0"
                    xml_output += f'      <binding name="{var_name}">\n'
                    xml_output += f'        <literal>{str(row)}</literal>\n'
                    xml_output += '      </binding>\n'
                
                xml_output += '    </result>\n'
            
            xml_output += '  </results>\n'
            xml_output += '</sparql>'
            
            return xml_output


@sparql_router.get("/")
async def sparql_get_endpoint(
    request: Request,
    query: Optional[str] = None,
    tenant_id: str = Depends(get_tenant_id),
    ontology_manager: Optional[UniversalOntologyManager] = Depends(get_tenant_ontology_manager)
):
    """
    W3C-compliant SPARQL endpoint (GET method).
    
    Args:
        request: The FastAPI request
        query: The SPARQL query string
        tenant_id: The tenant ID
        ontology_manager: The ontology manager for the tenant
        
    Returns:
        Query results in a format based on the Accept header
    """
    if not ontology_manager or not ontology_manager.world:
        raise HTTPException(status_code=404, detail="No ontology available")
    
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    # Create endpoint handler
    endpoint = FastAPIEndPoint(ontology_manager.world)
    
    # Get the Accept header
    accept_header = request.headers.get("accept", "application/sparql-results+json")
    
    # Handle the query
    return endpoint.handle_query(query, accept_header)


@sparql_router.post("/")
async def sparql_post_endpoint(
    request: Request,
    tenant_id: str = Depends(get_tenant_id),
    ontology_manager: Optional[UniversalOntologyManager] = Depends(get_tenant_ontology_manager)
):
    """
    W3C-compliant SPARQL endpoint (POST method).
    
    Args:
        request: The FastAPI request with the query in the body
        tenant_id: The tenant ID
        ontology_manager: The ontology manager for the tenant
        
    Returns:
        Query results in a format based on the Accept header
    """
    if not ontology_manager or not ontology_manager.world:
        raise HTTPException(status_code=404, detail="No ontology available")
    
    # Check content type
    content_type = request.headers.get("content-type", "")
    
    try:
        query_text = ""
        if "application/x-www-form-urlencoded" in content_type:
            form_data = await request.form()
            query_text = form_data.get("query", "")
        elif "application/sparql-query" in content_type:
            body_bytes = await request.body()
            query_text = body_bytes.decode("utf-8")
        else:
            # Try to parse as JSON
            body = await request.json()
            query_text = body.get("query", "")
        
        if not query_text:
            raise HTTPException(status_code=400, detail="Query is required in the request body")
        
        # Create endpoint handler
        endpoint = FastAPIEndPoint(ontology_manager.world)
        
        # Get the Accept header
        accept_header = request.headers.get("accept", "application/sparql-results+json")
        
        # Handle the query as string
        return endpoint.handle_query(str(query_text), accept_header)
        
    except Exception as e:
        logger.error(f"Error handling SPARQL request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing SPARQL request: {str(e)}") 