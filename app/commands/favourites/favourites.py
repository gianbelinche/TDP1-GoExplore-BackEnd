from typing import List
from app.commands.experiencies.errors import ExperienceNotFoundError
from app.commands.users.errors import UserNotFoundError
from app.models.favourite import Favourite
from app.models.user import User
from app.repositories.experience import ExperienceRepository
from app.schemas.experience import ExperienceSchema
from app.schemas.favourite import FavouriteSchema
from app.repositories import (
    UserRepository,
)
from app.config.logger import setup_logger

logger = setup_logger(__name__)


class AddFavouriteCommand:
    def __init__(
        self,
        user_repository: UserRepository,
        experience_repository: ExperienceRepository,
        user_id: str,
        favourite: FavouriteSchema,
    ):
        self.user_repository = user_repository
        self.experience_repository = experience_repository
        self.favourite = favourite
        self.user_id = user_id

    def execute(self) -> None:

        experience_id = self.favourite.experience_id
        user_id = self.user_id

        favourite = Favourite(user_id=user_id, experience_id=experience_id)

        user_exists = self.user_repository.user_exists(self.user_id)
        if not user_exists:
            raise UserNotFoundError

        experience_exists = self.experience_repository.experience_exists(experience_id)
        if not experience_exists:
            raise ExperienceNotFoundError

        self.user_repository.add_favourite(favourite)


class GetFavouritesCommand:
    def __init__(
        self,
        user_repository: UserRepository,
        experience_repository: ExperienceRepository,
        user_id: str,
    ):
        self.user_repository = user_repository
        self.experience_repository = experience_repository
        self.user_id = user_id

    def execute(self) -> List[ExperienceSchema]:
        user: User
        try:
            user = self.user_repository.get_user(self.user_id)
        except Exception:
            raise UserNotFoundError

        experiences = self.experience_repository.get_experiences_by_id(user.favourites)

        return list(map(lambda x: ExperienceSchema.from_model(x), experiences))


class DeleteFavouriteCommand:
    def __init__(
        self, user_repository: UserRepository, user_id: str, experience_id: str
    ):
        self.user_repository = user_repository
        self.experience_id = experience_id
        self.user_id = user_id

    def execute(self) -> None:
        user: User
        try:
            user = self.user_repository.get_user(self.user_id)
        except Exception:
            raise UserNotFoundError

        user.remove_favourite(self.experience_id)
        self.user_repository.update_user(user)
