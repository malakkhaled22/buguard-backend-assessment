from pydantic import BaseModel, ConfigDict


class TagCreate(BaseModel):
    name: str

class TagResponse(BaseModel):
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )