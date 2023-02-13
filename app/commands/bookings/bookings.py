from app.schemas.bookings import BookingCreateSchema, BookingSchema
from app.models.booking import Booking

from .errors import BookingAlreadyExistsError
from app.repositories import (
    BookingRepository,
)
from app.config.logger import setup_logger
import uuid

logger = setup_logger(__name__)


class CreateBookingCommand:
    def __init__(
        self, booking_repository: BookingRepository, booking: BookingCreateSchema
    ):
        self.booking_repository = booking_repository
        self.booking_data = booking

    def execute(self) -> BookingSchema:
        booking = Booking(
            experience_id=self.booking_data.experience_id,
            reserver_id=self.booking_data.reserver_id,
            date=self.booking_data.date,
            owner_id=self.booking_data.owner_id,
            id=str(uuid.uuid4()),
        )
        already_exists = self.booking_repository.booking_exists(
            booking.experience_id, booking.reserver_id
        )
        if already_exists:
            raise BookingAlreadyExistsError
        booking = self.booking_repository.add_booking(booking)

        return BookingSchema.from_model(booking)
