from sqlalchemy import Table, Column, Integer, String, ForeignKey
from app.database import Base


asset_tags = Table(
    "asset_tags",
    Base.metadata,

    Column(
        "asset_id",
        String,
        ForeignKey("assets.id")
    ),

    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id")
    )
)