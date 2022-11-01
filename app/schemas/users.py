from __future__ import annotations
from pydantic import BaseModel
from app.models.user import User


class UserSchemaBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    id: str


class UserCreateSchema(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    @classmethod
    def from_model(cls, user: User) -> UserSchema:
        return UserSchema(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            id=user.id if user.id else ""
        )
