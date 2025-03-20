"""
API routes for Ragatanga.

This module defines the FastAPI routes for the Ragatanga API.
"""

import os
import time
import traceback
import tempfile
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, Depends, Request, Response, Query
from fastapi.responses import HTMLResponse
from loguru import logger
import aiofiles

from ragatanga.api.models import (
    QueryRequest, 
    QueryResponse, 
    StatusResponse, 
    OntologyStatistics, 
    TenantCreateRequest, 
    TenantResponse,
    TenantUpdateRequest,
    TenantListResponse,
    RetrievedData,
    EntityInfo
)
from ragatanga.core.owl_retriever import UniversalOntologyManager
from ragatanga.core.semantic import SemanticSearch
from ragatanga.api.dependencies import (
    get_tenant_ontology_manager, 
    get_tenant_semantic_search,
    get_query_service
)
from ragatanga.api.auth import get_tenant_id
from ragatanga.models.tenant import tenant_store
from ragatanga.core.tenant import (
    tenant_ontology_manager,
    tenant_kb_manager
)
from ragatanga.api.services import QueryService
from ragatanga.exceptions import ConfigurationError
from ragatanga.utils.sparql import validate_sparql_query

# Create routers for different endpoint groups
core_router = APIRouter(tags=["core"])
tenant_router = APIRouter(prefix="/tenant", tags=["tenant"])
ontology_router = APIRouter(prefix="/ontology", tags=["ontology"])
kb_router = APIRouter(prefix="/knowledge-base", tags=["kb"])

@core_router.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint that displays system information and API documentation links.
    
    Returns:
        HTML page with system information
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ragatanga API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #2980b9;
                margin-top: 30px;
            }
            ul {
                margin-bottom: 20px;
            }
            li {
                margin-bottom: 8px;
            }
            code {
                background-color: #f7f7f7;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: 'Courier New', Courier, monospace;
            }
            .api-link {
                display: inline-block;
                background-color: #3498db;
                color: white;
                padding: 10px 15px;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 20px;
                font-weight: bold;
            }
            .api-link:hover {
                background-color: #2980b9;
            }
            .feature {
                background-color: #f8f9fa;
                border-left: 4px solid #3498db;
                padding: 15px;
                margin-bottom: 15px;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to Ragatanga API</h1>
        <p>
            Ragatanga is a hybrid knowledge retrieval system that combines semantic search and 
            SPARQL queries to provide comprehensive answers to natural language questions.
        </p>
        
        <a href="/docs" class="api-link">API Documentation</a>
        
        <h2>Key Features</h2>
        
        <div class="feature">
            <h3>Hybrid Retrieval</h3>
            <p>Combines semantic search and SPARQL queries for comprehensive results</p>
        </div>
        
        <div class="feature">
            <h3>Adaptive Weighting</h3>
            <p>Dynamically adjusts the weight of different retrieval methods based on query characteristics</p>
        </div>
        
        <div class="feature">
            <h3>Multi-Tenant Architecture</h3>
            <p>Supports isolated knowledge bases and ontologies for different tenants</p>
        </div>
        
        <div class="feature">
            <h3>Extensible Design</h3>
            <p>Pluggable architecture that supports different embedding and LLM providers</p>
        </div>
        
        <h2>Core Components</h2>
        <ul>
            <li><strong>Semantic Search Component</strong>: Performs vector-based semantic search using embeddings</li>
            <li><strong>SPARQL Query Component</strong>: Executes structured queries against the RDF knowledge graph</li>
            <li><strong>Ontology Manager Component</strong>: Manages the ontology and provides access to the knowledge graph</li>
            <li><strong>Adaptive Retriever Component</strong>: Coordinates between different retrieval methods</li>
            <li><strong>Query Processing Component</strong>: Handles user queries and generates structured answers</li>
        </ul>
        
        <h2>API Endpoints</h2>
        <ul>
            <li><code>POST /query</code>: Submit a natural language query</li>
            <li><code>GET /ontology/describe</code>: Get statistics about the ontology</li>
            <li><code>POST /ontology/upload</code>: Upload a new ontology file</li>
            <li><code>GET /ontology/download</code>: Download the current ontology</li>
            <li><code>POST /kb/upload</code>: Upload a new knowledge base file</li>
            <li><code>GET /kb/download</code>: Download the current knowledge base</li>
            <li><code>GET /tenant</code>: List all tenants</li>
            <li><code>POST /tenant</code>: Create a new tenant</li>
        </ul>
        
        <p>
            For complete API documentation and interactive testing, visit 
            <a href="/docs">the API docs</a>.
        </p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@core_router.get("/status", response_model=StatusResponse)
async def get_status(tenant_id: str = Depends(get_tenant_id)):
    """
    Get the current status of the Ragatanga API.
    
    Args:
        tenant_id: Validated tenant ID
        
    Returns:
        Status response with system information
    """
    # Get system information
    ontology_manager = tenant_ontology_manager.get_ontology_manager(tenant_id)
    semantic_search = tenant_kb_manager.get_semantic_search(tenant_id)
    
    # Count tenants
    tenant_count = len(tenant_store.list_tenants())
    
    # Check if components are initialized
    ontology_initialized = ontology_manager is not None
    kb_initialized = semantic_search is not None
    
    details = {
        "tenant_id": tenant_id,
        "tenant_count": tenant_count,
        "components": {
            "ontology_manager": True if ontology_initialized else False,
            "semantic_search": True if kb_initialized else False,
        }
    }
            
    return StatusResponse(
        message="Ragatanga API is operational",
        success=True,
        details=details
    )

@core_router.post("/query", response_model=QueryResponse)
async def handle_query(
    req: QueryRequest,
    tenant_id: str = Depends(get_tenant_id),
    query_service: QueryService = Depends(get_query_service)
):
    """
    Process a query for a specific tenant using the query service.
    
    Args:
        req: Query request with the user's query
        tenant_id: Validated tenant ID
        query_service: Service that handles query processing
        
    Returns:
        QueryResponse with answer and retrieved facts
    """
    try:
        return await query_service.process_query(tenant_id, req.query)
    except ConfigurationError as e:
        # Return user-friendly response for configuration issues
        return QueryResponse(
            answer=str(e.message),
            retrieval=RetrievedData(),
            entities=EntityInfo(),
            structured_data={"error": e.error_code},
            metadata={"success": False, "error_type": "configuration_error"}
        )
    except Exception as e:
        # Log unexpected errors and return appropriate status code
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@ontology_router.post("/upload", response_model=StatusResponse)
async def upload_ontology(
    file: UploadFile,
    tenant_id: str = Depends(get_tenant_id),
    ontology_manager: Optional[UniversalOntologyManager] = Depends(get_tenant_ontology_manager)
):
    """
    Upload a new ontology file (.ttl or .owl) for a specific tenant.
    
    Args:
        file: Uploaded file
        tenant_id: Validated tenant ID
        ontology_manager: Current tenant ontology manager (may be None)
        
    Returns:
        Status response
    """
    if not file.filename or not file.filename.endswith(('.ttl', '.owl')):
        raise HTTPException(status_code=400, detail="File must be .ttl or .owl")
    
    try:
        contents = await file.read()
        try:
            decoded_contents = contents.decode('utf-8')
        except UnicodeDecodeError:
            decoded_contents = contents.decode('latin-1')
        
        # Create a new file path for the uploaded ontology
        from ragatanga.config import DATA_DIR
        tenant_dir = os.path.join(DATA_DIR, "tenants", tenant_id)
        os.makedirs(tenant_dir, exist_ok=True)
        
        upload_filename = f"ontology_{int(time.time())}_{file.filename}"
        new_ontology_path = os.path.join(tenant_dir, upload_filename)
        
        # Save the new ontology file
        async with aiofiles.open(new_ontology_path, "w", encoding='utf-8') as out_file:
            await out_file.write(decoded_contents)
        
        # Add the ontology to the tenant
        # Store the result but don't use it here as we're returning a different response
        _ = tenant_store.add_ontology(
            tenant_id=tenant_id,
            name=file.filename,
            file_path=new_ontology_path,
            description=f"Uploaded on {datetime.now().isoformat()}"
        )
        
        # Reload both ontology managers
        legacy_success = await tenant_ontology_manager.reload_ontology(tenant_id, force_rebuild=True)
        
        logger.info(f"Ontology updated for tenant {tenant_id}: {new_ontology_path}")
        logger.info(f"Legacy ontology manager reload: {legacy_success}")
        
        return StatusResponse(
            message="Ontology uploaded and loaded successfully",
            success=True,
            details={
                "file_name": file.filename, 
                "ontology_path": new_ontology_path,
                "tenant_id": tenant_id
            }
        )
    except Exception as e:
        logger.error(f"Error uploading ontology for tenant {tenant_id}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error uploading ontology: {str(e)}")

@ontology_router.get("/download")
async def download_ontology(
    tenant_id: str = Depends(get_tenant_id),
    ontology_manager: Optional[UniversalOntologyManager] = Depends(get_tenant_ontology_manager)
):
    """
    Download the active ontology for a tenant.
    
    Args:
        tenant_id: Validated tenant ID
        ontology_manager: Tenant-specific ontology manager
        
    Returns:
        Ontology file download
    """
    if not ontology_manager:
        raise HTTPException(
            status_code=404, 
            detail="No ontology configured for this tenant"
        )
    
    tenant_ontology = tenant_store.get_active_ontology(tenant_id)
    if not tenant_ontology:
        raise HTTPException(
            status_code=404,
            detail="No active ontology found for this tenant"
        )
    
    try:
        file_path = tenant_ontology.file_path
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Ontology file not found")
        
        # Create a temporary file to save the ontology in the preferred format
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
            tmp_path = tmp.name
        
        # Save the ontology using the save method with rdfxml format
        success = ontology_manager.save(
            output_path=tmp_path, 
            format="rdfxml"
        )
        
        if not success:
            # Fallback to original method if save fails
            async with aiofiles.open(file_path, "r") as f:
                content = await f.read()
        else:
            # Read the saved file
            async with aiofiles.open(tmp_path, "r") as f:
                content = await f.read()
            # Clean up the temporary file
            os.unlink(tmp_path)
        
        # Set the filename to a tenant-specific name with appropriate extension
        filename = f"tenant_{tenant_id}_ontology.xml"
        
        return Response(
            content=content,
            media_type="application/rdf+xml",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"Error downloading ontology: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading ontology: {str(e)}")

@kb_router.post("/upload", response_model=StatusResponse)
async def upload_knowledge_base(
    file: UploadFile,
    tenant_id: str = Depends(get_tenant_id),
    semantic_search: Optional[SemanticSearch] = Depends(get_tenant_semantic_search)
):
    """
    Upload a new knowledge base file (.md) for a specific tenant.
    
    Args:
        file: Uploaded file
        tenant_id: Validated tenant ID
        semantic_search: Current tenant semantic search (may be None)
        
    Returns:
        Status response
    """
    if not file.filename or not file.filename.endswith(('.md', '.txt')):
        raise HTTPException(status_code=400, detail="File must be .md or .txt")
    
    try:
        contents = await file.read()
        try:
            decoded_contents = contents.decode('utf-8')
        except UnicodeDecodeError:
            decoded_contents = contents.decode('latin-1')
        
        # Create a new file path for the uploaded knowledge base
        from ragatanga.config import DATA_DIR
        tenant_dir = os.path.join(DATA_DIR, "tenants", tenant_id)
        os.makedirs(tenant_dir, exist_ok=True)
        
        upload_filename = f"kb_{int(time.time())}_{file.filename}"
        new_kb_path = os.path.join(tenant_dir, upload_filename)
        
        # Save the new knowledge base file
        async with aiofiles.open(new_kb_path, "w", encoding='utf-8') as out_file:
            await out_file.write(decoded_contents)
        
        # Add the knowledge base to the tenant
        # Store the result but don't use it here as we're returning a different response
        _ = tenant_store.add_knowledge_base(
            tenant_id=tenant_id,
            name=file.filename,
            file_path=new_kb_path,
            description=f"Uploaded on {datetime.now().isoformat()}"
        )
        
        # Reload knowledge base
        await tenant_kb_manager.reload_knowledge_base(tenant_id, force_rebuild=True)
        
        logger.info(f"Knowledge base updated for tenant {tenant_id}: {new_kb_path}")
        
        return StatusResponse(
            message="Knowledge base uploaded and processed successfully",
            success=True,
            details={
                "file_name": file.filename,
                "kb_path": new_kb_path,
                "tenant_id": tenant_id
            }
        )
    except Exception as e:
        logger.error(f"Error uploading knowledge base for tenant {tenant_id}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error uploading knowledge base: {str(e)}")

@kb_router.get("/download")
async def download_knowledge_base(
    tenant_id: str = Depends(get_tenant_id)
):
    """
    Download the active knowledge base for a tenant.
    
    Args:
        tenant_id: Validated tenant ID
        
    Returns:
        Knowledge base file download
    """
    tenant_kb = tenant_store.get_active_knowledge_base(tenant_id)
    if not tenant_kb:
        raise HTTPException(
            status_code=404,
            detail="No active knowledge base found for this tenant"
        )
    
    try:
        file_path = tenant_kb.file_path
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Knowledge base file not found")
        
        async with aiofiles.open(file_path, "r") as f:
            content = await f.read()
        
        # Set the filename to a tenant-specific name
        filename = f"tenant_{tenant_id}_kb_{os.path.basename(file_path)}"
        
        return Response(
            content=content,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading knowledge base: {str(e)}")

@ontology_router.get("/describe", response_model=OntologyStatistics)
async def describe_ontology(
    tenant_id: str = Depends(get_tenant_id),
    ontology_manager: Optional[UniversalOntologyManager] = Depends(get_tenant_ontology_manager),
    debug: bool = Query(False, description="Include debugging information in response")
):
    """
    Get statistics about the active ontology for a tenant.
    
    Args:
        tenant_id: Validated tenant ID
        ontology_manager: Tenant-specific ontology manager
        debug: Whether to include debug information
        
    Returns:
        Statistics about the ontology structure
    """
    if not ontology_manager:
        raise HTTPException(status_code=404, detail="No ontology configured for this tenant")
    
    try:
        # Get statistics directly from the ontology manager
        stats = ontology_manager.get_ontology_structure()
        
        # If debug is True, include debug information
        if not debug and "debug_info" in stats.get("metadata", {}):
            del stats["metadata"]["debug_info"]
        
        logger.info(f"Returning ontology statistics: {stats}")
        
        # Return the OntologyStatistics model
        return OntologyStatistics(
            statistics=stats.get("statistics", {}),
            classes=stats.get("classes", {}),
            properties=stats.get("properties", {}),
            individuals=stats.get("individuals", {}),
            metadata=stats.get("metadata", {})
        )
    except Exception as e:
        logger.error(f"Error getting ontology statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting ontology statistics: {str(e)}")

@ontology_router.post("/sparql", response_model=Dict[str, Any])
async def execute_sparql_query(
    request: Request,
    tenant_id: str = Depends(get_tenant_id),
    ontology_manager: Optional[UniversalOntologyManager] = Depends(get_tenant_ontology_manager)
):
    """
    Execute a SPARQL query against the tenant's ontology.
    
    Args:
        request: FastAPI request object with the SPARQL query
        tenant_id: Validated tenant ID
        ontology_manager: Tenant-specific ontology manager
        
    Returns:
        Query results
    """
    if not ontology_manager:
        raise HTTPException(status_code=404, detail="No ontology configured for this tenant")
    
    # Parse the JSON body to get the query
    try:
        body = await request.json()
        query = body.get("query", "")
        parameters = body.get("parameters", None)
        validate_query = body.get("validate", True)
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Validate the query syntax if requested
        if validate_query:
            is_valid, error_message = validate_sparql_query(query)
            
            if not is_valid:
                return {
                    "error": "Invalid SPARQL query syntax",
                    "details": error_message,
                    "success": False
                }
            
        # Execute the query using correct method
        results = await ontology_manager.execute_query(query, parameters)
        
        return {
            "results": results,
            "count": len(results),
            "success": True
        }
    except Exception as e:
        logger.error(f"Error executing SPARQL query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error executing SPARQL query: {str(e)}")

@tenant_router.get("/", response_model=TenantListResponse)
async def list_tenants():
    """
    List all tenants (admin endpoint).
    
    Returns:
        List of tenants
    """
    try:
        tenants = tenant_store.list_tenants()
        return TenantListResponse(
            tenants=[
                TenantResponse(
                    id=tenant.id,
                    name=tenant.name,
                    created_at=tenant.created_at.isoformat(),
                    updated_at=tenant.updated_at.isoformat(),
                    metadata=tenant.metadata
                ) 
                for tenant in tenants
            ]
        )
    except Exception as e:
        logger.error(f"Error listing tenants: {str(e)}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Error listing tenants: {str(e)}")

@tenant_router.post("/", response_model=TenantResponse)
async def create_tenant(
    tenant_data: TenantCreateRequest
):
    """
    Create a new tenant (admin endpoint).
    
    Args:
        tenant_data: The tenant creation data
        
    Returns:
        The created tenant
    """
    try:
        tenant = tenant_store.create_tenant(
            name=tenant_data.name, 
            metadata=tenant_data.metadata
        )
        return TenantResponse(
            id=tenant.id,
            name=tenant.name,
            created_at=tenant.created_at.isoformat(),
            updated_at=tenant.updated_at.isoformat(),
            metadata=tenant.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating tenant: {str(e)}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Failed to create tenant: {str(e)}")

@tenant_router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(tenant_id: str):
    """
    Get a specific tenant by ID (admin endpoint).
    
    Args:
        tenant_id: The ID of the tenant to retrieve
        
    Returns:
        The tenant details
    """
    try:
        tenant = tenant_store.get_tenant(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail=f"Tenant with ID {tenant_id} not found")
        
        return TenantResponse(
            id=tenant.id,
            name=tenant.name,
            created_at=tenant.created_at.isoformat(),
            updated_at=tenant.updated_at.isoformat(),
            metadata=tenant.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving tenant: {str(e)}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tenant: {str(e)}")

@tenant_router.patch("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: str, 
    tenant_data: TenantUpdateRequest
):
    """
    Update tenant metadata (admin endpoint).
    
    Args:
        tenant_id: The ID of the tenant to update
        tenant_data: The data to update
        
    Returns:
        The updated tenant details
    """
    try:
        tenant = tenant_store.get_tenant(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail=f"Tenant with ID {tenant_id} not found")
        
        # Update name if provided
        if tenant_data.name:
            tenant.name = tenant_data.name
        
        # Update or add metadata fields if provided
        if tenant_data.metadata:
            tenant.metadata.update(tenant_data.metadata)
        
        # Update timestamp
        tenant.updated_at = datetime.now()
        
        return TenantResponse(
            id=tenant.id,
            name=tenant.name,
            created_at=tenant.created_at.isoformat(),
            updated_at=tenant.updated_at.isoformat(),
            metadata=tenant.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating tenant: {str(e)}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Failed to update tenant: {str(e)}")


# The /universal-query endpoint has been removed since its functionality
# is now integrated into the main /query endpoint