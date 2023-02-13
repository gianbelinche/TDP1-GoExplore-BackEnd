from app.repositories.config import db
from abc import ABC, abstractmethod
from app.models.booking import Booking

# from app.repositories.errors import BookingNotFoundError


class BookingRepository(ABC):
    @abstractmethod
    def add_booking(self, booking: Booking) -> Booking:
        pass

    @abstractmethod
    def booking_exists(self, id: str) -> bool:
        pass


class PersistentBookingRepository(BookingRepository):
    def __init__(self):
        COLLECTION_NAME = "Bookings"
        self.bookings = db[COLLECTION_NAME]

    def add_booking(self, booking: Booking) -> Booking:
        data = self.__serialize_booking(booking)
        self.bookings.insert_one(data)
        return booking

    def booking_exists(self, experience_id: str, reserver_id: str) -> bool:
        booking = self.bookings.find_one(
            {'experience_id': experience_id, 'reserver_id': reserver_id}
        )
        return booking is not None

    def __serialize_booking(self, booking: Booking) -> dict:
        serialized = {
            '_id': booking.id,
            "experience_id": booking.experience_id,
            "reserver_id": booking.reserver_id,
            "date": booking.date,
            "owner_id": booking.owner_id,
        }

        return serialized

    def __deserialize_booking(self, data: dict) -> Booking:

        return Booking(
            id=data['_id'],
            experience_id=data['experience_id'],
            reserver_id=data['reserver_id'],
            date=data['date'],
            owner_id=data['owner_id'],
        )
