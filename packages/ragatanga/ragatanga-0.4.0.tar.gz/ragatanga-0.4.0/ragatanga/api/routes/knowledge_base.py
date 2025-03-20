"""
Knowledge base routes module.

This module defines the API routes for knowledge base management.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ragatanga.schemas.knowledge_base import KnowledgeBase, KnowledgeBaseCreate, KnowledgeBaseUpdate
from ragatanga.services.knowledge_base import KnowledgeBaseService
from ragatanga.api.dependencies import get_knowledge_base_service

router = APIRouter()


@router.post("/", response_model=KnowledgeBase, status_code=status.HTTP_201_CREATED)
async def create_knowledge_base(
    kb_data: KnowledgeBaseCreate,
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    """
    Create a new knowledge base.
    """
    try:
        return await kb_service.create_knowledge_base(kb_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/tenant/{tenant_id}", response_model=List[KnowledgeBase])
async def get_tenant_knowledge_bases(
    tenant_id: UUID,
    active_only: bool = False,
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    """
    Get all knowledge bases for a tenant.
    """
    if active_only:
        return await kb_service.get_active_knowledge_bases(tenant_id)
    return await kb_service.get_tenant_knowledge_bases(tenant_id)


@router.get("/ontology/{ontology_id}", response_model=List[KnowledgeBase])
async def get_knowledge_bases_by_ontology(
    ontology_id: UUID,
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    """
    Get all knowledge bases that use a specific ontology.
    """
    return await kb_service.get_knowledge_bases_by_ontology(ontology_id)


@router.get("/{kb_id}", response_model=KnowledgeBase)
async def get_knowledge_base(
    kb_id: UUID,
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    """
    Get a knowledge base by ID.
    """
    kb = await kb_service.get_knowledge_base(kb_id)
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base with ID {kb_id} not found",
        )
    return kb


@router.put("/{kb_id}", response_model=KnowledgeBase)
async def update_knowledge_base(
    kb_id: UUID,
    kb_data: KnowledgeBaseUpdate,
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    """
    Update a knowledge base.
    """
    try:
        kb = await kb_service.update_knowledge_base(kb_id, kb_data)
        if not kb:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Knowledge base with ID {kb_id} not found",
            )
        return kb
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{kb_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge_base(
    kb_id: UUID,
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    """
    Delete a knowledge base.
    """
    deleted = await kb_service.delete_knowledge_base(kb_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base with ID {kb_id} not found",
        )


@router.post("/{kb_id}/activate", response_model=KnowledgeBase)
async def activate_knowledge_base(
    kb_id: UUID,
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    """
    Activate a knowledge base.
    """
    kb = await kb_service.activate_knowledge_base(kb_id)
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base with ID {kb_id} not found",
        )
    return kb


@router.post("/{kb_id}/deactivate", response_model=KnowledgeBase)
async def deactivate_knowledge_base(
    kb_id: UUID,
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    """
    Deactivate a knowledge base.
    """
    kb = await kb_service.deactivate_knowledge_base(kb_id)
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base with ID {kb_id} not found",
        )
    return kb


@router.post("/{kb_id}/index", response_model=KnowledgeBase)
async def index_knowledge_base(
    kb_id: UUID,
    kb_service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    """
    Index a knowledge base and update its statistics.
    """
    kb = await kb_service.index_knowledge_base(kb_id)
    if not kb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Knowledge base with ID {kb_id} not found",
        )
    return kb 