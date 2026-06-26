from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.asset import Asset
from app.services.ai_service import assess_asset_risk

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post("/risk/{asset_id}")
def get_risk_assessment(
    asset_id: str,
    db: Session = Depends(get_db)
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

    result = assess_asset_risk(asset)

    return {
        "asset_id": asset.id,
        "assessment": result
    }