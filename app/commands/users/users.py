from app.schemas.users import UserCreateSchema, UserSchema
from app.models.user import User
from .errors import UserAlreadyExistsError, UserNotFoundError
from app.repositories import (
    UserRepository,
)
from app.config.logger import setup_logger

logger = setup_logger(__name__)


class CreateUserCommand():
    def __init__(
        self,
        user_repository: UserRepository,
        user: UserCreateSchema
    ):
        self.user_repository = user_repository
        self.user_data = user

    def execute(self) -> UserSchema:
        user = User(
            first_name=self.user_data.first_name,
            last_name=self.user_data.last_name,
            email=self.user_data.email,
            id=self.user_data.id
        )
        already_exists = self.user_repository.user_exists(user.id)
        if already_exists:
            raise UserAlreadyExistsError
        user = self.user_repository.add_user(user)

        return UserSchema.from_model(user)


class GetUserCommand():
    def __init__(
        self,
        user_repository: UserRepository,
        _id: str
    ):
        self.user_repository = user_repository
        self.id = _id

    def execute(self) -> UserSchema:

        exists = self.user_repository.user_exists(self.id)
        if not exists:
            raise UserNotFoundError
        user = self.user_repository.get_user(self.id)

        return UserSchema.from_model(user)
