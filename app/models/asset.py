from sqlalchemy import Column, String, DateTime, JSON, UniqueConstraint
from app.database import Base
from datetime import UTC, datetime
import uuid

from app.enums.asset_enum import AssetType, AssetStatus

from sqlalchemy.orm import relationship
from app.models.asset_tag import asset_tags

class Asset(Base):
    __tablename__ = "assets"

    __table_args__ = (
        UniqueConstraint(
            "type",
            "value",
            name="unique_asset_type_value"
        ),
    )
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    type = Column(String, nullable=False)

    value = Column(String, nullable=False)

    status = Column(
        String,
        default=AssetStatus.ACTIVE.value
    )

    source = Column(String)

    asset_metadata = Column(JSON)

    first_seen = Column(
        DateTime,
        default=datetime.now(UTC)
    )

    last_seen = Column(
        DateTime,
        default=datetime.now(UTC)
    )

    tags = relationship(
        "Tag",
        secondary="asset_tags",
        back_populates="assets"
    )