from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr
from app.models.user import User


class UserSchemaBase(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    email: EmailStr
    id: str = Field(..., min_length=1)


class UserCreateSchema(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    @classmethod
    def from_model(cls, user: User) -> UserSchema:
        return UserSchema(
            first_name=user.first_name,
            last_name=user.last_name,
            email=EmailStr(user.email),
            id=user.id if user.id else ""
        )
