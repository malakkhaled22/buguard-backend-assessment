from pydantic import BaseModel, ConfigDict
from typing import (Optional, List)

from app.enums.asset_enum import AssetType
from app.schemas.tag_schema import TagResponse


class AssetCreate(BaseModel):
    type: AssetType
    value: str
    source: Optional[str] = None
    tags: List[str] = []
    metadata: dict = {}
    

class AssetResponse(BaseModel):
    id: str
    type: AssetType
    value: str
    status: str
    source: str | None = None

    asset_metadata: dict | None = None

    tags: List[TagResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )

class AssetUpdate(BaseModel):
    type: AssetType
    value: str
    source: str | None = None
    status: str | None = None

class BulkImportRequest(BaseModel):
    assets: List[AssetCreate]
