from pydantic import BaseModel, ConfigDict


class RelationshipCreate(BaseModel):
    source_asset_id: str
    target_asset_id: str
    relationship_type: str

class RelationshipResponse(BaseModel):
    id: int
    source_asset_id: str
    target_asset_id: str
    relationship_type: str

    model_config = ConfigDict(
        from_attributes=True
    )