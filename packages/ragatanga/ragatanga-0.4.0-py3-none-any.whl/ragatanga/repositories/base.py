"""
Base repository class for Ragatanga.

This module defines the base repository class that all other repositories will inherit from.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel

from ragatanga.schemas.base import BaseSchema

# Define a type variable for the schema model
T = TypeVar('T', bound=BaseSchema)


class BaseRepository(Generic[T], ABC):
    """
    Base repository class for all Ragatanga repositories.
    
    Provides common CRUD operations for working with schema models.
    """
    
    def __init__(self, model_class: Type[T]):
        """
        Initialize the repository with the model class.
        
        Args:
            model_class: The Pydantic model class this repository handles
        """
        self.model_class = model_class
    
    @abstractmethod
    async def create(self, data: Union[Dict[str, Any], BaseModel]) -> T:
        """
        Create a new record.
        
        Args:
            data: The data to create the record with
            
        Returns:
            The created record
        """
        pass
    
    @abstractmethod
    async def get(self, id: UUID) -> Optional[T]:
        """
        Get a record by ID.
        
        Args:
            id: The ID of the record to get
            
        Returns:
            The record if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def get_all(self, **filters) -> List[T]:
        """
        Get all records matching the given filters.
        
        Args:
            **filters: Filters to apply
            
        Returns:
            A list of matching records
        """
        pass
    
    @abstractmethod
    async def update(self, id: UUID, data: Union[Dict[str, Any], BaseModel]) -> Optional[T]:
        """
        Update a record.
        
        Args:
            id: The ID of the record to update
            data: The data to update the record with
            
        Returns:
            The updated record if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a record.
        
        Args:
            id: The ID of the record to delete
            
        Returns:
            True if the record was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a record exists.
        
        Args:
            id: The ID of the record to check
            
        Returns:
            True if the record exists, False otherwise
        """
        pass 