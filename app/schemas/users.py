from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr
from app.models.user import User


class UserSchemaBase(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=3)
    birth_date: str = Field(..., min_length=3)


class UserCreateSchema(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    id: str = Field(..., min_length=1)
    cards: list = Field(...)

    @classmethod
    def from_model(cls, user: User) -> UserSchema:
        return UserSchema(
            first_name=user.first_name,
            last_name=user.last_name,
            email=EmailStr(user.email),
            id=user.id if user.id else "",
            password=user.password,
            birth_date=user.birth_date,
            cards=user.cards,
        )
