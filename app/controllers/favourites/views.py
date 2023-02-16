from fastapi.exceptions import HTTPException
from app.commands.favourites.favourites import AddFavouriteCommand, GetFavouritesCommand
from app.repositories.experience import PersistentExperienceRepository
from typing import List
from fastapi import status, APIRouter
from app.config.logger import setup_logger
from app.repositories.users import PersistentUserRepository
from app.schemas.experience import (
    ExperienceSchema,
)
from app.schemas.favourite import FavouriteSchema
from app.utils.error import GoExploreError


logger = setup_logger(name=__name__)
router = APIRouter()


@router.post(
    '/users/{user_id}/favourites',
    status_code=status.HTTP_201_CREATED,
    response_model=FavouriteSchema,
)
async def add_favourite(user_id: str, favourite_body: FavouriteSchema):
    try:
        user_repository = PersistentUserRepository()
        experience_repository = PersistentExperienceRepository()
        AddFavouriteCommand(
            user_repository, experience_repository, user_id, favourite_body
        ).execute()

        return favourite_body
    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )


@router.get(
    '/users/{user_id}/favourites',
    status_code=status.HTTP_200_OK,
    response_model=List[ExperienceSchema],
)
async def get_favourites(user_id: str):
    try:
        user_repository = PersistentUserRepository()
        experience_repository = PersistentExperienceRepository()
        favourites = GetFavouritesCommand(
            user_repository, experience_repository, user_id
        ).execute()

    except GoExploreError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error"
        )

    return favourites
