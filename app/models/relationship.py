from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True)

    source_asset_id = Column(
        String,
        ForeignKey("assets.id")
    )

    target_asset_id = Column(
        String,
        ForeignKey("assets.id")
    )

    relationship_type = Column(String)