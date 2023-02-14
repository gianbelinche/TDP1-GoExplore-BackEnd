from __future__ import annotations
from pydantic import BaseModel, Field, ValidationError, root_validator
from datetime import date
from typing import List, Optional
from app.models.experience import Experience, Category


class SearchExperience(BaseModel):
    lat: Optional[float]
    lng: Optional[float]
    dist: int = Field(default=10000)
    owner: Optional[str]
    category: Optional[Category]
    limit: int = Field(default=5)


class LocationSchema(BaseModel):
    description: str = Field(..., min_length=3)
    lat: float
    lng: float


class ExperienceSchemaBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)
    price: int
    score: Optional[float] = Field(default=0.0)
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
            score=experience.score,
            location=location,
            category=Category(experience.category),
            images=experience.images,
            preview_image=experience.preview_image,
            availability=experience.availability,
            owner=experience.owner,
            id=experience.id,
        )
