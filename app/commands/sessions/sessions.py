from app.schemas.sessions import SessionCreateSchema, SessionSchema
from .errors import UserNotFoundError, IncorrectPasswordError
from app.repositories import (
    UserRepository,
)
from app.config.logger import setup_logger

logger = setup_logger(__name__)


class CreateSessionCommand:
    def __init__(self, user_repository: UserRepository, session: SessionCreateSchema):
        self.user_repository = user_repository
        self.session_data = session

    def execute(self) -> SessionSchema:
        already_exists = self.user_repository.user_exists_by_email(
            self.session_data.email
        )
        if not already_exists:
            raise UserNotFoundError
        user = self.user_repository.get_user_by_email(self.session_data.email)
        if user.password != self.session_data.password:
            raise IncorrectPasswordError

        return SessionSchema.from_model()
