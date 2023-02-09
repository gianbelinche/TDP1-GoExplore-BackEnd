from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr


class SessionSchemaBase(BaseModel):
    pass


class SessionCreateSchema(SessionSchemaBase):
    email: EmailStr
    password: str = Field(..., min_length=3)


class SessionSchema(SessionSchemaBase):
    session: bool

    @classmethod
    def from_model(cls) -> SessionSchema:
        return SessionSchema(session=True)
