from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.relationship import Relationship


def create_relationship(
    relationship,
    db: Session
):

    source_asset = (
        db.query(Asset)
        .filter(
            Asset.id == relationship.source_asset_id
        )
        .first()
    )

    target_asset = (
        db.query(Asset)
        .filter(
            Asset.id == relationship.target_asset_id
        )
        .first()
    )

    if not source_asset or not target_asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    new_relationship = Relationship(
        source_asset_id=relationship.source_asset_id,
        target_asset_id=relationship.target_asset_id,
        relationship_type=relationship.relationship_type
    )

    db.add(new_relationship)

    db.commit()

    db.refresh(new_relationship)

    return new_relationship


def get_relationships(
    db: Session
):
    return (
        db.query(Relationship)
        .all()
    )