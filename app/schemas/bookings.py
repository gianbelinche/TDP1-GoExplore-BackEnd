from __future__ import annotations
from pydantic import BaseModel, Field
from app.models.booking import Booking


class BookingSchemaBase(BaseModel):
    experience_id: str = Field(..., min_length=3)
    reserver_id: str = Field(..., min_length=3)
    owner_id: str = Field(..., min_length=3)
    date: str = Field(..., min_length=3)
    amount: int
    guests: int = Field(...)


class BookingCreateSchema(BookingSchemaBase):
    pass


class BookingSchema(BookingSchemaBase):
    id: str = Field(..., min_length=1)

    @classmethod
    def from_model(cls, booking: Booking) -> BookingSchema:
        return BookingSchema(
            experience_id=booking.experience_id,
            reserver_id=booking.reserver_id,
            owner_id=booking.owner_id,
            date=booking.date,
            amount=booking.amount,
            id=booking.id,
            guests=booking.guests,
        )
