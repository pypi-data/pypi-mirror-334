"""
Main entry point for the Ragatanga API.

This module provides a simple way to start the Ragatanga API server
and initialize user data for pip-installed deployments.
"""

import os
import sys
import shutil
import argparse
import uvicorn
from loguru import logger
from typing import Optional

from ragatanga import config
from ragatanga.api.app import app
from ragatanga.core.tenant import setup_default_tenant
from ragatanga.models.tenant import tenant_store

def initialize_user_data(force=False):
    """
    Initialize user data directory with sample files.
    
    Args:
        force: Whether to overwrite existing files
    """
    logger.info(f"Initializing user data directory: {config.USER_DATA_DIR}")
    
    # Copy sample files
    sample_files = [
        "sample_ontology_owl.ttl",
        "sample_knowledge_base.md"
    ]
    
    for filename in sample_files:
        src = os.path.join(config.PACKAGE_DATA_DIR, filename)
        dst = os.path.join(config.USER_DATA_DIR, filename)
        
        if os.path.exists(src) and (force or not os.path.exists(dst)):
            try:
                shutil.copy2(src, dst)
                logger.info(f"Copied sample file: {filename}")
            except Exception as e:
                logger.error(f"Error copying {filename}: {str(e)}")
        elif not os.path.exists(src):
            logger.warning(f"Source file not found: {src}")
    
    logger.info("Initialization complete!")
    logger.info("You can now run 'ragatanga-server' to start the API server")

async def init_tenant_system():
    """Initialize the tenant system with a default tenant."""
    logger.info("Initializing tenant system...")
    
    # Check if there's already a default tenant
    tenants = tenant_store.list_tenants()
    if tenants:
        logger.info(f"Tenant system already initialized with {len(tenants)} tenants")
        return
    
    # Create default tenant
    default_tenant = tenant_store.create_tenant(
        name="Default",
        metadata={"description": "Default tenant created during initialization"}
    )
    logger.info(f"Created default tenant with ID: {default_tenant.id}")
    
    # Set up the default tenant with sample data
    await setup_default_tenant()
    
    logger.info("Tenant system initialized successfully")

def run_server(host: str = "127.0.0.1", port: Optional[int] = None):
    """
    Run the Ragatanga API server.
    
    Args:
        host: Host to bind to. Defaults to 127.0.0.1 for security reasons.
            Use 0.0.0.0 to bind to all interfaces, but only in controlled environments.
        port: Port to bind to. If None, use default port from config.
    """
    effective_port = port or config.DEFAULT_PORT or 8000
    logger.info(f"Starting Ragatanga API server on {host}:{effective_port}")
    uvicorn.run(app, host=host, port=effective_port)

def cli_init():
    """Command-line entry point for initialization."""
    parser = argparse.ArgumentParser(description="Initialize Ragatanga data directory")
    parser.add_argument("--force", action="store_true", help="Force overwrite of existing files")
    args = parser.parse_args()
    
    initialize_user_data(force=args.force)
    
def cli_server():
    """Command-line entry point for server."""
    parser = argparse.ArgumentParser(description="Run Ragatanga API server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to. Use 0.0.0.0 to bind to all interfaces.")
    parser.add_argument("--port", type=int, default=None, help="Port to bind to")
    args = parser.parse_args()
    
    run_server(host=args.host, port=args.port)

if __name__ == "__main__":
    # For local development
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        initialize_user_data(force="--force" in sys.argv)
    else:
        run_server()