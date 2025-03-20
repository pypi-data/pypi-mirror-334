"""
Ontology routes module.

This module defines the API routes for ontology management.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ragatanga.schemas.ontology import Ontology, OntologyCreate, OntologyUpdate
from ragatanga.services.ontology import OntologyService
from ragatanga.api.dependencies import get_ontology_service

router = APIRouter()


@router.post("/", response_model=Ontology, status_code=status.HTTP_201_CREATED)
async def create_ontology(
    ontology_data: OntologyCreate,
    ontology_service: OntologyService = Depends(get_ontology_service),
):
    """
    Create a new ontology.
    """
    try:
        return await ontology_service.create_ontology(ontology_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/tenant/{tenant_id}", response_model=List[Ontology])
async def get_tenant_ontologies(
    tenant_id: UUID,
    active_only: bool = False,
    ontology_service: OntologyService = Depends(get_ontology_service),
):
    """
    Get all ontologies for a tenant.
    """
    if active_only:
        return await ontology_service.get_active_ontologies(tenant_id)
    return await ontology_service.get_tenant_ontologies(tenant_id)


@router.get("/{ontology_id}", response_model=Ontology)
async def get_ontology(
    ontology_id: UUID,
    ontology_service: OntologyService = Depends(get_ontology_service),
):
    """
    Get an ontology by ID.
    """
    ontology = await ontology_service.get_ontology(ontology_id)
    if not ontology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ontology with ID {ontology_id} not found",
        )
    return ontology


@router.put("/{ontology_id}", response_model=Ontology)
async def update_ontology(
    ontology_id: UUID,
    ontology_data: OntologyUpdate,
    ontology_service: OntologyService = Depends(get_ontology_service),
):
    """
    Update an ontology.
    """
    try:
        ontology = await ontology_service.update_ontology(ontology_id, ontology_data)
        if not ontology:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ontology with ID {ontology_id} not found",
            )
        return ontology
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{ontology_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ontology(
    ontology_id: UUID,
    ontology_service: OntologyService = Depends(get_ontology_service),
):
    """
    Delete an ontology.
    """
    deleted = await ontology_service.delete_ontology(ontology_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ontology with ID {ontology_id} not found",
        )


@router.post("/{ontology_id}/activate", response_model=Ontology)
async def activate_ontology(
    ontology_id: UUID,
    ontology_service: OntologyService = Depends(get_ontology_service),
):
    """
    Activate an ontology.
    """
    ontology = await ontology_service.activate_ontology(ontology_id)
    if not ontology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ontology with ID {ontology_id} not found",
        )
    return ontology


@router.post("/{ontology_id}/deactivate", response_model=Ontology)
async def deactivate_ontology(
    ontology_id: UUID,
    ontology_service: OntologyService = Depends(get_ontology_service),
):
    """
    Deactivate an ontology.
    """
    ontology = await ontology_service.deactivate_ontology(ontology_id)
    if not ontology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ontology with ID {ontology_id} not found",
        )
    return ontology


@router.post("/{ontology_id}/analyze", response_model=Ontology)
async def analyze_ontology(
    ontology_id: UUID,
    ontology_service: OntologyService = Depends(get_ontology_service),
):
    """
    Analyze an ontology and update its statistics.
    """
    ontology = await ontology_service.analyze_ontology(ontology_id)
    if not ontology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ontology with ID {ontology_id} not found",
        )
    return ontology 