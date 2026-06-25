import pytest
from sqlalchemy import text
from app.database import SessionLocal
from app.models.asset import Asset
from app.models.relationship import Relationship
from app.models.tag import Tag
from datetime import datetime, timezone

datetime.now(timezone.utc)
@pytest.fixture(autouse=True)
def clean_db():
    db = SessionLocal()

    try:
        db.execute(text("DELETE FROM asset_tags"))

        db.query(Relationship).delete()

        db.query(Tag).delete()

        db.query(Asset).delete()

        db.commit()

        yield

    finally:
        db.close()