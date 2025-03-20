"""
SQLAlchemy table definitions.

This module defines the SQLAlchemy tables for the Ragatanga database.
"""

from datetime import datetime

from sqlalchemy import (
    Column, Table, MetaData, String, Boolean, Integer, DateTime, JSON, ForeignKey,
    text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

# Create metadata object
metadata = MetaData()

# Create an alias for declarative_base
Base = declarative_base(metadata=metadata)

# Define UUID column type that works with both PostgreSQL and SQLite
def UUIDColumn(name: str, primary_key: bool = False, nullable: bool = False, foreign_key=None) -> Column:
    """
    Create a UUID column that works with both PostgreSQL and SQLite.
    
    Args:
        name: The name of the column
        primary_key: Whether the column is a primary key
        nullable: Whether the column is nullable
        foreign_key: Optional foreign key reference
        
    Returns:
        A SQLAlchemy Column
    """
    if primary_key:
        # For Supabase, use server-side UUID generation for primary keys
        default = None
        server_default = text("gen_random_uuid()")
    else:
        default = None
        server_default = None
        
    # Use native UUID for PostgreSQL which is what Supabase uses
    column_args = {
        "primary_key": primary_key,
        "default": default,
        "server_default": server_default,
        "nullable": nullable,
    }
    
    # Add foreign key if provided
    if foreign_key:
        column_args["foreign_key"] = ForeignKey(foreign_key, ondelete="CASCADE")
        
    return Column(name, UUID(as_uuid=True), **column_args)


# Define tenant table
tenant_table = Table(
    "tenants",
    metadata,
    UUIDColumn("id", primary_key=True),
    Column("name", String(100), nullable=False, index=True),
    Column("description", String(500), nullable=True),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("metadata", JSON, nullable=False, default={}),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=True, onupdate=datetime.now),
    Column("ontology_count", Integer, nullable=False, default=0),
    Column("knowledge_base_count", Integer, nullable=False, default=0),
)

# Define ontology table
ontology_table = Table(
    "ontologies",
    metadata,
    UUIDColumn("id", primary_key=True),
    Column("tenant_id", UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
    Column("name", String(200), nullable=False, index=True),
    Column("description", String(1000), nullable=True),
    Column("file_path", String(500), nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("metadata", JSON, nullable=False, default={}),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=True, onupdate=datetime.now),
    Column("last_accessed", DateTime, nullable=True),
    Column("stats", JSON, nullable=True),
)

# Define knowledge base table
knowledge_base_table = Table(
    "knowledge_bases",
    metadata,
    UUIDColumn("id", primary_key=True),
    Column("tenant_id", UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
    Column("name", String(200), nullable=False, index=True),
    Column("description", String(1000), nullable=True),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("embedding_model", String(100), nullable=False, index=True),
    Column("chunk_size", Integer, nullable=False, default=1000),
    Column("chunk_overlap", Integer, nullable=False, default=200),
    Column("metadata", JSON, nullable=False, default={}),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=True, onupdate=datetime.now),
    Column("last_updated", DateTime, nullable=True),
    Column("last_accessed", DateTime, nullable=True),
    Column("stats", JSON, nullable=True),
) 