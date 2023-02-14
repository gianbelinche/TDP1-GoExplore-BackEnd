from fastapi.exceptions import HTTPException
from app.repositories.users import PersistentUserRepository
from fastapi import status, APIRouter
from app.config.logger import setup_logger
from app.schemas.users import UserCreateSchema, UserSchema, CardCreateSchema
from app.commands.users import CreateUserCommand, GetUserCommand, UpdateUserCommand
from app.utils.error import GoExploreError
from app.schemas.bookings import BookingSchema
from typing import List
from app.commands.bookings import (
    GetBookingsByReserverCommand,
    GetBookingsByOwnerCommand,
)
from app.repositories.bookings import PersistentBookingRepository


logger = setup_logger(name=__name__)
router = APIRouter()


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user(user_body: UserCreateSchema):
    try:
        repository = PersistentUserRepository()
        user = CreateUserCommand(repository, user_body).execute()
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )
    return user


@router.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user(id: str):
    try:
        repository = PersistentUserRepository()
        user = GetUserCommand(repository, id).execute()
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )

    return user


@router.post(
    '/users/{id}/card', status_code=status.HTTP_201_CREATED, response_model=UserSchema
)
async def add_card(id: str, card_body: CardCreateSchema):
    try:
        repository = PersistentUserRepository()
        user = UpdateUserCommand(repository, card_body, id).execute()
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )
    return user


@router.get(
    '/users/{id}/bookings_reserved',
    status_code=status.HTTP_200_OK,
    response_model=List[BookingSchema],
)
async def get_user_bookings_reserved(id: str):
    try:
        repository = PersistentBookingRepository()
        bookings = GetBookingsByReserverCommand(repository, id).execute()
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )

    return bookings


@router.get(
    '/users/{id}/bookings_received',
    status_code=status.HTTP_200_OK,
    response_model=List[BookingSchema],
)
async def get_user_bookings_received(id: str):
    try:
        repository = PersistentBookingRepository()
        bookings = GetBookingsByOwnerCommand(repository, id).execute()
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )

    return bookings
