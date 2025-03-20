"""
Configuration package for the Ragatanga application.

This package contains configuration settings for the application.
"""

import sys
import importlib.util
from typing import Optional, Callable, Any

# Define the fallback function
def _fallback_get_data_file(filename: str, subdirectory: Optional[str] = None) -> str:
    """Fallback implementation of get_data_file."""
    import os
    from pathlib import Path
    
    # Define directories
    BASE_DIR = Path(__file__).resolve().parent.parent
    PACKAGE_DATA_DIR = os.path.join(BASE_DIR, "data")
    USER_DATA_DIR = os.path.join(Path.home(), ".ragatanga")
    
    if subdirectory:
        user_path = os.path.join(USER_DATA_DIR, subdirectory, filename)
        package_path = os.path.join(PACKAGE_DATA_DIR, subdirectory, filename)
    else:
        user_path = os.path.join(USER_DATA_DIR, filename)
        package_path = os.path.join(PACKAGE_DATA_DIR, filename)
    
    # Check user path first
    if os.path.exists(user_path):
        return user_path
    
    # Then check package path
    if os.path.exists(package_path):
        return package_path
    
    # Return user path even if it doesn't exist yet
    return user_path

# Try to import get_data_file from the root config module
try:
    # Check if the module exists
    if importlib.util.find_spec('ragatanga.config'):
        # Import the module
        config_module = importlib.import_module('ragatanga.config')
        # Get the function
        _imported_get_data_file = getattr(config_module, 'get_data_file', None)
        if _imported_get_data_file is not None:
            get_data_file = _imported_get_data_file
        else:
            get_data_file = _fallback_get_data_file
except (ImportError, AttributeError):
    get_data_file = _fallback_get_data_file

from ragatanga.config.settings import (
    BASE_DIR,
    DATA_DIR,
    TENANT_DIR,
    PACKAGE_DATA_DIR,
    USER_DATA_DIR,
    DATABASE_URL,
    DB_ECHO,
    API_PREFIX,
    API_DEBUG,
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    DEFAULT_PORT,
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CHUNK_OVERLAP,
    LOG_LEVEL,
    LOG_FORMAT
)

__all__ = [
    "BASE_DIR",
    "DATA_DIR",
    "TENANT_DIR",
    "PACKAGE_DATA_DIR",
    "USER_DATA_DIR",
    "DATABASE_URL",
    "DB_ECHO",
    "API_PREFIX",
    "API_DEBUG",
    "API_TITLE",
    "API_DESCRIPTION",
    "API_VERSION",
    "DEFAULT_PORT",
    "CORS_ORIGINS",
    "CORS_ALLOW_CREDENTIALS",
    "CORS_ALLOW_METHODS",
    "CORS_ALLOW_HEADERS",
    "DEFAULT_EMBEDDING_MODEL",
    "DEFAULT_CHUNK_SIZE",
    "DEFAULT_CHUNK_OVERLAP",
    "LOG_LEVEL",
    "LOG_FORMAT",
    "get_data_file"
] 