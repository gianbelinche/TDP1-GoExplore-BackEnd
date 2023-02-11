from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import date
from typing import List
from app.models.experience import Experience, Category


class LocationSchema(BaseModel):
    description: str = Field(..., min_length=3)
    lat: float
    lng: float


class ExperienceSchemaBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)
    price: int
    location: LocationSchema
    category: Category
    images: List[str] = Field(..., min_length=1)
    preview_image: str = Field(..., min_length=1)
    availability: List[date] = Field(..., min_items=2, max_items=2)
    owner: str = Field(..., min_length=1)


class ExperienceCreateSchema(ExperienceSchemaBase):
    pass


class ExperienceSchema(ExperienceSchemaBase):
    id: str = Field(..., min_length=1)

    @classmethod
    def from_model(cls, experience: Experience) -> ExperienceSchema:
        location = LocationSchema(
            description=experience.location.description,
            lat=experience.location.lat,
            lng=experience.location.lng,
        )

        return ExperienceSchema(
            title=experience.title,
            description=experience.description,
            price=experience.price,
            location=location,
            category=Category(experience.category),
            images=experience.images,
            preview_image=experience.preview_image,
            availability=experience.availability,
            owner=experience.owner,
            id=experience.id,
        )
