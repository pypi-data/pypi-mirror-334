import os
from pathlib import Path
from loguru import logger

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Package data directory (read-only)
PACKAGE_DATA_DIR = os.path.join(BASE_DIR, "data")

# User data directory (writable)
USER_DATA_DIR = os.path.join(Path.home(), ".ragatanga")
os.makedirs(USER_DATA_DIR, exist_ok=True)

# Ensure tenant directory exists
TENANT_DIR = os.path.join(USER_DATA_DIR, "tenants")
os.makedirs(TENANT_DIR, exist_ok=True)

# For backward compatibility with existing code, use USER_DATA_DIR as DATA_DIR
DATA_DIR = USER_DATA_DIR

# Helper function to get a data file, checking user directory first, then package
def get_data_file(filename, subdirectory=None):
    """
    Get the path to a data file, checking user directory first, then package.
    
    Args:
        filename: The filename to look for
        subdirectory: Optional subdirectory within the data directory
        
    Returns:
        The path to the file (user path even if it doesn't exist yet)
    """
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

# Look for environment variable first, then try user directory, then package directory
env_ontology_path = os.getenv("OWL_FILE_PATH")

# Determine the ontology path with clear logging
if env_ontology_path and os.path.exists(env_ontology_path):
    # Use the environment variable if it exists and the file exists
    ONTOLOGY_PATH = env_ontology_path
    logger.info(f"Using ontology from environment variable: {ONTOLOGY_PATH}")
else:
    # Check user directory first, then package
    ONTOLOGY_PATH = get_data_file("sample_ontology_owl.ttl")
    if os.path.exists(ONTOLOGY_PATH):
        logger.info(f"Using ontology from: {ONTOLOGY_PATH}")
    else:
        logger.warning(f"No ontology found. Will use path: {ONTOLOGY_PATH} when it becomes available")
    
    # Set the environment variable to ensure consistency
    os.environ["OWL_FILE_PATH"] = ONTOLOGY_PATH

# Set knowledge base path similarly
env_kb_path = os.getenv("KNOWLEDGE_BASE_PATH")
if env_kb_path and os.path.exists(env_kb_path):
    KNOWLEDGE_BASE_PATH = env_kb_path
    logger.info(f"Using knowledge base from environment variable: {KNOWLEDGE_BASE_PATH}")
else:
    KNOWLEDGE_BASE_PATH = get_data_file("sample_knowledge_base.md")
    logger.info(f"Using knowledge base: {KNOWLEDGE_BASE_PATH}")

# Create index path in user directory
KBASE_INDEX_PATH = os.path.join(USER_DATA_DIR, "kbase_index.pkl")

# SPARQL configuration
SPARQL_ENDPOINT_MEMORY = "memory://"
SPARQL_ENDPOINT_FILE = f"file://{ONTOLOGY_PATH}"

# Semantic search configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Question answering configuration
MAX_TOKENS = 8000
TEMPERATURE = 0.7 

# Embedding configuration
EMBED_MODEL = "text-embedding-3-large"
BATCH_SIZE = 16
DIMENSIONS = 3072

# LLM configuration
DEFAULT_LLM_MODEL = "gpt-4o"

# API configuration
DEFAULT_PORT = 8000