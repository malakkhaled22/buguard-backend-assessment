from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models.asset import Asset
from app.models.relationship import Relationship
from app.schemas.relationship_schema import (
    RelationshipCreate,
    RelationshipResponse
)
from app.services.relationship_service import create_relationship, get_relationships

router = APIRouter(
    prefix="/relationships",
    tags=["Relationships"]
)

@router.post(
    "/",
    response_model=RelationshipResponse
)
def create_relationship_route(
    relationship: RelationshipCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    return create_relationship(relationship, db)

@router.get(
    "/",
    response_model=list[RelationshipResponse]
)
def get_relationships_route(
    db: Session = Depends(get_db)
):
    return get_relationships(db)