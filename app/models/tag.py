from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.asset_tag import asset_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    assets = relationship(
        "Asset",
        secondary="asset_tags",
        back_populates="tags"
    )