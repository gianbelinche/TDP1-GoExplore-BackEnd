from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from app.models.experience import Experience


class ExperienceSchemaBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)
    images: list[str] = Field(..., min_length=1)
    preview_image: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)


class ExperienceCreateSchema(ExperienceSchemaBase):
    calendar: dict
    id: Optional[str]
    pass


class ExperienceSchema(ExperienceSchemaBase):
    calendar: list
    id: str

    @classmethod
    def from_model(cls, experience: Experience) -> ExperienceSchema:
        return ExperienceSchema(
            title=experience.title,
            description=experience.description,
            images=experience.images,
            preview_image=experience.preview_image,
            calendar=experience.calendar,
            owner=experience.owner,
            id=experience.id,
        )
