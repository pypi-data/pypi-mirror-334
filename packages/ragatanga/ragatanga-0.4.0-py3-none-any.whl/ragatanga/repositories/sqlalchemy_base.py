"""
SQLAlchemy implementation of the base repository.

This module provides a SQLAlchemy-based implementation of the base repository.
"""

from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Table, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ragatanga.repositories.base import BaseRepository
from ragatanga.schemas.base import BaseSchema

# Define a type variable for the schema model
T = TypeVar('T', bound=BaseSchema)


class SQLAlchemyRepository(BaseRepository[T], Generic[T]):
    """
    SQLAlchemy implementation of the base repository.
    
    Provides CRUD operations using SQLAlchemy for database access.
    """
    
    def __init__(self, model_class: Type[T], table: Table, session: AsyncSession):
        """
        Initialize the repository with the model class, table, and session.
        
        Args:
            model_class: The Pydantic model class this repository handles
            table: The SQLAlchemy table for this model
            session: The SQLAlchemy async session
        """
        super().__init__(model_class)
        self.table = table
        self.session = session
    
    async def create(self, data: Union[Dict[str, Any], BaseModel]) -> T:
        """
        Create a new record.
        
        Args:
            data: The data to create the record with
            
        Returns:
            The created record
        """
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_unset=True)
        
        # Set created_at timestamp
        if 'created_at' not in data:
            data['created_at'] = datetime.now()
        
        # Insert the record
        stmt = insert(self.table).values(**data).returning(*self.table.c)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        # Convert to model
        record = result.fetchone()
        return self.model_class(**dict(record))
    
    async def get(self, id: UUID) -> Optional[T]:
        """
        Get a record by ID.
        
        Args:
            id: The ID of the record to get
            
        Returns:
            The record if found, None otherwise
        """
        stmt = select(self.table).where(self.table.c.id == id)
        result = await self.session.execute(stmt)
        record = result.fetchone()
        
        if record is None:
            return None
        
        return self.model_class(**dict(record))
    
    async def get_all(self, **filters) -> List[T]:
        """
        Get all records matching the given filters.
        
        Args:
            **filters: Filters to apply
            
        Returns:
            A list of matching records
        """
        stmt = select(self.table)
        
        # Apply filters
        for key, value in filters.items():
            if hasattr(self.table.c, key):
                stmt = stmt.where(getattr(self.table.c, key) == value)
        
        result = await self.session.execute(stmt)
        records = result.fetchall()
        
        return [self.model_class(**dict(record)) for record in records]
    
    async def update(self, id: UUID, data: Union[Dict[str, Any], BaseModel]) -> Optional[T]:
        """
        Update a record.
        
        Args:
            id: The ID of the record to update
            data: The data to update the record with
            
        Returns:
            The updated record if found, None otherwise
        """
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_unset=True)
        
        # Set updated_at timestamp
        data['updated_at'] = datetime.now()
        
        # Update the record
        stmt = (
            update(self.table)
            .where(self.table.c.id == id)
            .values(**data)
            .returning(*self.table.c)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        # Convert to model
        record = result.fetchone()
        if record is None:
            return None
        
        return self.model_class(**dict(record))
    
    async def delete(self, id: UUID) -> bool:
        """
        Delete a record.
        
        Args:
            id: The ID of the record to delete
            
        Returns:
            True if the record was deleted, False otherwise
        """
        stmt = delete(self.table).where(self.table.c.id == id).returning(self.table.c.id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        return result.fetchone() is not None
    
    async def exists(self, id: UUID) -> bool:
        """
        Check if a record exists.
        
        Args:
            id: The ID of the record to check
            
        Returns:
            True if the record exists, False otherwise
        """
        stmt = select(self.table.c.id).where(self.table.c.id == id)
        result = await self.session.execute(stmt)
        
        return result.fetchone() is not None 