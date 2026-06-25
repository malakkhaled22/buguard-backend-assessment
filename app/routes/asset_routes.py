from sqlalchemy.orm import Session
from fastapi import (Depends, HTTPException, APIRouter)
from app.auth import verify_api_key
from app.database import get_db
from app.models.asset import Asset
from app.models.tag import Tag
from app.schemas.asset_schema import (AssetCreate, AssetUpdate, BulkImportRequest, AssetResponse, TagResponse)
from app.models.relationship import Relationship

from typing import Optional
from datetime import UTC, datetime

from app.services.asset_service import create_asset, delete_asset, get_asset_by_id, get_asset_tags, get_assets, get_related_assets, import_assets, mark_asset_stale, update_asset

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)

@router.post("/")
def create_asset_route(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    return create_asset(asset, db)

@router.get(
        "/",
        response_model=list[AssetResponse]
)
def get_assets_route(
    type: Optional[str] = None,
    status: Optional[str] = None,
    value: Optional[str] = None,
    tag: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_assets(
        db=db,
        type=type,
        status=status,
        value=value,
        tag=tag,
        page=page,
        limit=limit,
        sort_by=sort_by
    )

@router.get(
        "/{asset_id}",
        response_model=AssetResponse
)
def get_asset_route(
    asset_id: str,
    db: Session = Depends(get_db)
):
    return get_asset_by_id(asset_id, db)

@router.delete("/{asset_id}")
def delete_asset_route(
    asset_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    return delete_asset(asset_id, db)

@router.put("/{asset_id}")
def update_asset_route(
    asset_id: str,
    asset_data: AssetUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    return update_asset(asset_id, asset_data, db)

@router.post("/import")
def import_assets_route(
    data: BulkImportRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    return import_assets(data, db)

@router.get("/{asset_id}/tags")
def get_asset_tags_route(
    asset_id: str,
    db: Session = Depends(get_db)
):
    return get_asset_tags(asset_id, db)

@router.get("/{asset_id}/related")
def get_related_assets_route(
    asset_id: str,
    db: Session = Depends(get_db)
): 
    return get_related_assets(asset_id, db)

@router.patch("/{asset_id}/mark-stale")
def mark_asset_stale_route(
    asset_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    return mark_asset_stale(asset_id, db)