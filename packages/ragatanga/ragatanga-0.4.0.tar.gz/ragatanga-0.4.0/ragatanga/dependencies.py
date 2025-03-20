"""
Dependencies for resolving import issues.

This module attempts to install required dependencies if they are missing.
"""

import subprocess  # nosec B404 - We validate package names before using subprocess
import sys
import importlib.util
import re
from typing import List, Set


# Define a whitelist of allowed packages
ALLOWED_PACKAGES: Set[str] = {
    "sqlalchemy",
    "aiosqlite",
    "fastapi",
    "pydantic",
    "uvicorn",
    "psycopg[binary,pool]",
    "psycopg[binary]",
    "psycopg[pool]",
    "psycopg",
    "owlready2",
    "faiss-cpu",
    "sentence-transformers",
    "transformers",
    "torch",
    "numpy",
    "pandas",
    "requests",
    "aiohttp",
    "httpx",
    "loguru",
    "python-jose",
    "python-multipart",
    "psycopg2-binary",
    "asyncpg",
}


def is_valid_package_name(package_name: str) -> bool:
    """
    Validate that a package name is safe to install.
    
    Args:
        package_name: Name of the package to validate
        
    Returns:
        True if the package name is valid and in the whitelist, False otherwise
    """
    # Check if package is in whitelist
    if package_name not in ALLOWED_PACKAGES:
        print(f"Package {package_name} is not in the allowed packages list")
        return False
    
    # Additional validation: package names should only contain alphanumeric, -, _, ., [, ]
    # This allows for packages with extras like psycopg[binary]
    if not re.match(r'^[a-zA-Z0-9_\-\.\[\],]+$', package_name):
        print(f"Package name {package_name} contains invalid characters")
        return False
        
    return True


def check_import(package_name: str) -> bool:
    """
    Check if a package can be imported.
    
    Args:
        package_name: Name of the package to check
        
    Returns:
        True if the package can be imported, False otherwise
    """
    return importlib.util.find_spec(package_name.split('[')[0]) is not None


def install_package(package_name: str) -> bool:
    """
    Install a package using pip.
    
    Args:
        package_name: Name of the package to install
        
    Returns:
        True if installation was successful, False otherwise
    """
    # Validate package name before installation
    if not is_valid_package_name(package_name):
        print(f"Refusing to install package with invalid or unauthorized name: {package_name}")
        return False
        
    try:
        # We've validated the package name is safe, so this subprocess call is secure
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])  # nosec B603
        return True
    except subprocess.CalledProcessError:
        return False


def ensure_dependencies(dependencies: List[str]) -> None:
    """
    Ensure that all dependencies are installed.
    
    Args:
        dependencies: List of package names to check and install if missing
    """
    for package in dependencies:
        if not check_import(package.split('[')[0]):  # Handle packages with extras like psycopg[binary]
            print(f"Installing missing dependency: {package}")
            if install_package(package):
                print(f"Successfully installed {package}")
            else:
                print(f"Failed to install {package}")


# Define required dependencies - must be in ALLOWED_PACKAGES
required_dependencies = [
    "sqlalchemy",
    "aiosqlite",
    "fastapi",
    "pydantic",
    "uvicorn",
    "psycopg[binary,pool]"  # PostgreSQL adapter for Supabase
]

# Check and install dependencies when this module is imported
ensure_dependencies(required_dependencies) 