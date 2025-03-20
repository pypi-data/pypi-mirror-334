# Ragatanga

Ragatanga is a knowledge management system that combines ontology-based knowledge representations with semantic search capabilities.

## Architecture

The application follows a layered architecture pattern:

1. **API Layer** (`ragatanga/api`): FastAPI routes and API-specific dependencies.
2. **Service Layer** (`ragatanga/services`): Business logic and orchestration.
3. **Repository Layer** (`ragatanga/repositories`): Data access and persistence.
4. **Schema Layer** (`ragatanga/schemas`): Data validation and serialization.
5. **Database Layer** (`ragatanga/database`): Database configuration and connection management.
6. **Configuration** (`ragatanga/config`): Application settings and configuration.

## Installation

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install 'sqlalchemy[asyncio]' aiosqlite fastapi uvicorn pydantic
```

### Optional Dependencies

For enhanced text chunking capabilities, install Chonkie:

```bash
pip install chonkie
```

This provides advanced text chunking methods including:
- Recursive chunking
- Sentence-based chunking
- Token-based chunking
- Paragraph-based chunking
- Markdown-aware chunking

## Running the Application

Start the application using Uvicorn:

```bash
uvicorn ragatanga.api.app:app --reload
```

This will start the API server with hot-reloading enabled for development.

## Main Entities

### Tenant

A tenant represents an organization or user of the system. Each tenant can have multiple ontologies and knowledge bases.

### Ontology

An ontology defines the structure of knowledge for a specific domain. It includes classes, properties, and relationships between entities.

### Knowledge Base

A knowledge base contains documents and data that are processed and indexed for semantic search.

## API Endpoints

The API is organized around the following resources:

- `/api/tenants`: Tenant management
- `/api/ontologies`: Ontology management
- `/api/knowledge-bases`: Knowledge base management

## Text Processing

Ragatanga includes several text processing utilities:

- **Text Chunking**: Split large documents into smaller chunks for processing
  - Legacy chunking method (default)
  - Advanced chunking methods via Chonkie integration (when installed)
- **Text Similarity**: Compute similarity between text strings
- **Text Cleaning**: Normalize and clean text for processing

## Development

### Project Structure

```
ragatanga/
├── api/
│   ├── routes/
│   ├── app.py
│   ├── dependencies.py
│   └── router.py
├── config/
│   └── settings.py
├── database/
│   ├── session.py
│   └── tables.py
├── repositories/
│   ├── base.py
│   ├── tenant.py
│   ├── ontology.py
│   └── knowledge_base.py
├── schemas/
│   ├── base.py
│   ├── tenant.py
│   ├── ontology.py
│   └── knowledge_base.py
└── services/
    ├── tenant.py
    ├── ontology.py
    └── knowledge_base.py
```

### Release Process

Ragatanga follows a structured release process:

1. **Version Update**: Update version numbers in:
   - `pyproject.toml`
   - `setup.py`
   - `ragatanga/__init__.py`
   - `ragatanga/_version.py` (if exists)

2. **Changelog**: Update `docs/changelog.md` with details about the new release.

3. **Automated Release**: Use the release script to package and publish:
   ```bash
   python scripts/release.py
   ```
   
   For testing on TestPyPI first:
   ```bash
   python scripts/release.py --test
   ```

4. **GitHub Release**: The GitHub Actions workflow will automatically create a release when a new tag is pushed.

5. **Documentation**: Ensure documentation is updated for the new version.

## License

MIT
