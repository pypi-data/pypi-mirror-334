"""
Base schema classes for Ragatanga.

This module defines the base schema classes for the Ragatanga application.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """
    Base schema class for all Ragatanga models.
    
    Provides common fields and configuration for all models.
    """
    
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    model_config = {
        "json_schema_extra": {
            "description": "Base schema for all Ragatanga models"
        },
        "json_encoders": {
            datetime: lambda dt: dt.isoformat(),
            UUID: lambda id: str(id),
        },
        "from_attributes": True,  # Replaces orm_mode
    }

    def dict_with_extras(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Convert the model to a dictionary with additional fields.
        
        Args:
            **kwargs: Additional fields to include in the dictionary.
            
        Returns:
            Dict[str, Any]: Model as a dictionary with additional fields.
        """
        model_dict = self.model_dump()
        model_dict.update(kwargs)
        return model_dict 