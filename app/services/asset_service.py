from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import UTC, datetime

from app.models import tag
from app.models.asset import Asset
from app.models.tag import Tag
from app.models.relationship import Relationship


def create_asset(asset_data, db: Session):

    new_asset = Asset(
        type=asset_data.type,
        value=asset_data.value,
        source=asset_data.source,
        asset_metadata=asset_data.metadata
    )

    for tag_name in asset_data.tags:

        tag = (
            db.query(Tag)
            .filter(Tag.name == tag_name)
            .first()
        )

        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()

        new_asset.tags.append(tag)

    db.add(new_asset)

    db.commit()

    db.refresh(new_asset)

    return new_asset


def get_asset_by_id(
    asset_id: str,
    db: Session
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


def get_assets(
    db: Session,
    type=None,
    status=None,
    value=None,
    tag=None,
    page=1,
    limit=10,
    sort_by=None
):
    assets = db.query(Asset)

    if type:
        assets = assets.filter(
            Asset.type == type
        )

    if status:
        assets = assets.filter(
            Asset.status == status
        )

    if value:
        assets = assets.filter(
            Asset.value.ilike(f"%{value}%")
        )


    if tag:
        assets = assets.filter(
            Asset.tags.any(Tag.name == tag)
        )
    
    
    if sort_by == "last_seen":
        assets = assets.order_by(
            Asset.last_seen.desc()
        )


    elif sort_by == "first_seen":
        assets = assets.order_by(
            Asset.first_seen.desc()
        )

    elif sort_by == "value":
        assets = assets.order_by(
            Asset.value.asc()
        )

    offset = (page - 1) * limit

    assets = assets.offset(offset).limit(limit)

    return assets.all()


def update_asset(
    asset_id,
    asset_data,
    db: Session
):

    asset = get_asset_by_id(
        asset_id,
        db
    )

    asset.type = asset_data.type
    asset.value = asset_data.value
    asset.source = asset_data.source

    if asset_data.status:
        asset.status = asset_data.status

    db.commit()

    db.refresh(asset)

    return asset


def delete_asset(
    asset_id: str,
    db: Session
):

    asset = get_asset_by_id(
        asset_id,
        db
    )

    db.delete(asset)

    db.commit()

    return {
        "message": "Asset deleted successfully"
    }


def import_assets(
    data,
    db: Session
):

    imported = 0
    updated = 0

    for asset_data in data.assets:

        existing_asset = (
            db.query(Asset)
            .filter(
                Asset.type == asset_data.type,
                Asset.value == asset_data.value
            )
            .first()
        )

        if existing_asset:

            existing_asset.last_seen = datetime.now(UTC)
            existing_asset.status = "active"

            current_metadata = dict(
                existing_asset.asset_metadata or {}
            )

            current_metadata.update(
                asset_data.metadata or {}
            )

            existing_asset.asset_metadata = current_metadata

            for tag_name in asset_data.tags:

                tag = (
                    db.query(Tag)
                    .filter(Tag.name == tag_name)
                    .first()
                )

                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.flush()

                if tag not in existing_asset.tags:
                    existing_asset.tags.append(tag)

            updated += 1

        else:

            new_asset = Asset(
                type=asset_data.type,
                value=asset_data.value,
                source=asset_data.source,
                asset_metadata=asset_data.metadata
            )

            db.add(new_asset)

            db.flush()

            for tag_name in asset_data.tags:

                tag = (
                    db.query(Tag)
                    .filter(Tag.name == tag_name)
                    .first()
                )

                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.flush()

                if tag not in new_asset.tags:
                    new_asset.tags.append(tag)

            imported += 1

    db.commit()

    return {
        "imported": imported,
        "updated": updated
    }


def get_asset_tags(
    asset_id,
    db: Session
):

    asset = get_asset_by_id(
        asset_id,
        db
    )

    return [
        tag.name
        for tag in asset.tags
    ]


def get_related_assets(
    asset_id,
    db: Session
):

    asset = get_asset_by_id(
        asset_id,
        db
    )

    relationships = (
        db.query(Relationship)
        .filter(
            (Relationship.source_asset_id == asset_id) |
            (Relationship.target_asset_id == asset_id)
        )
        .all()
    )

    related_assets = []

    for relationship in relationships:

        if relationship.source_asset_id == asset_id:
            other_asset_id = relationship.target_asset_id
        else:
            other_asset_id = relationship.source_asset_id

        related_asset = (
            db.query(Asset)
            .filter(Asset.id == other_asset_id)
            .first()
        )

        related_assets.append({
            "relationship_type": relationship.relationship_type,
            "related_asset": related_asset
        })

    return {
        "asset": asset,
        "related_assets": related_assets
    }


def mark_asset_stale(
    asset_id,
    db: Session
):

    asset = get_asset_by_id(
        asset_id,
        db
    )

    asset.status = "stale"

    db.commit()

    db.refresh(asset)

    return {
        "message": "Asset marked as stale",
        "asset": asset
    }