"""
Application settings module.

This module defines the configuration settings for the Ragatanga application.
Settings can be overridden using environment variables.
"""

import os

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get("RAGATANGA_DATA_DIR", os.path.join(BASE_DIR, "data"))
TENANT_DIR = os.path.join(DATA_DIR, "tenants")
PACKAGE_DATA_DIR = os.path.join(BASE_DIR, "data")
USER_DATA_DIR = os.environ.get("RAGATANGA_USER_DATA_DIR", os.path.expanduser("~/.ragatanga"))

# Database
DATABASE_URL = os.environ.get("RAGATANGA_DATABASE_URL", "sqlite+aiosqlite:///ragatanga.db")
DB_ECHO = os.environ.get("RAGATANGA_DB_ECHO", "False").lower() == "true"

# API
API_PREFIX = os.environ.get("RAGATANGA_API_PREFIX", "/api")
API_DEBUG = os.environ.get("RAGATANGA_API_DEBUG", "False").lower() == "true"
API_TITLE = os.environ.get("RAGATANGA_API_TITLE", "Ragatanga API")
API_DESCRIPTION = os.environ.get("RAGATANGA_API_DESCRIPTION", "API for the Ragatanga knowledge management system")
API_VERSION = os.environ.get("RAGATANGA_API_VERSION", "0.1.0")
DEFAULT_PORT = int(os.environ.get("RAGATANGA_PORT", "8000"))

# CORS
CORS_ORIGINS = os.environ.get("RAGATANGA_CORS_ORIGINS", "*").split(",")
CORS_ALLOW_CREDENTIALS = os.environ.get("RAGATANGA_CORS_ALLOW_CREDENTIALS", "True").lower() == "true"
CORS_ALLOW_METHODS = os.environ.get("RAGATANGA_CORS_ALLOW_METHODS", "*").split(",")
CORS_ALLOW_HEADERS = os.environ.get("RAGATANGA_CORS_ALLOW_HEADERS", "*").split(",")

# Knowledge Base
DEFAULT_EMBEDDING_MODEL = os.environ.get("RAGATANGA_DEFAULT_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
DEFAULT_CHUNK_SIZE = int(os.environ.get("RAGATANGA_DEFAULT_CHUNK_SIZE", "1000"))
DEFAULT_CHUNK_OVERLAP = int(os.environ.get("RAGATANGA_DEFAULT_CHUNK_OVERLAP", "200"))

# Logging
LOG_LEVEL = os.environ.get("RAGATANGA_LOG_LEVEL", "INFO")
LOG_FORMAT = os.environ.get(
    "RAGATANGA_LOG_FORMAT", 
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) 