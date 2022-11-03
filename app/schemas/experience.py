from __future__ import annotations
from pydantic import BaseModel, Field
from app.models.experience import Experience


class ExperienceSchemaBase(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)
    images: list[str] = Field(..., min_length=1)
    preview_image: str = Field(..., min_length=1)
    calendar: dict
    owner: str = Field(..., min_length=1)
    id: str = Field(..., min_length=1)


class ExperienceCreateSchema(ExperienceSchemaBase):
    pass


class ExperienceSchema(ExperienceSchemaBase):
    @classmethod
    def from_model(cls, experience: Experience) -> ExperienceSchema:
        return ExperienceSchema(
            title=experience.title,
            description=experience.description,
            images=experience.images,
            preview_image=experience.preview_image,
            calendar=experience.calendar,
            owner=experience.owner,
            id=experience.id if experience.id else "",
        )
