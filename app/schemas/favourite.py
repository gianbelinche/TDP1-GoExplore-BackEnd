from pydantic import BaseModel, Field


class FavouriteSchema(BaseModel):
    experience_id: str = Field(..., min_length=3)
