from fastapi import FastAPI
from app.database import engine, Base

from app.models.asset import Asset
from app.models.tag import Tag
from app.models.relationship import Relationship

from app.models.asset_tag import asset_tags

from app.routes.asset_routes import router as asset_router
from app.routes.relationship_routes import router as relationship_routes
from app.routes.ai_routes import router as ai_router
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(asset_router)
app.include_router(relationship_routes)
app.include_router(ai_router)

@app.get("/")
def home():
    return {"message": "Asset Management API"}