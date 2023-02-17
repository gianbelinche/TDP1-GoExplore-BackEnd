from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr

from app.models.user import User


class SessionSchemaBase(BaseModel):
    pass


class SessionCreateSchema(SessionSchemaBase):
    email: EmailStr
    password: str = Field(..., min_length=3)


class SessionSchema(SessionSchemaBase):
    id: str

    @classmethod
    def from_model(cls, user: User) -> SessionSchema:
        return SessionSchema(id=user.id)
