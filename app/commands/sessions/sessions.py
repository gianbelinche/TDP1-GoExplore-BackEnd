from app.models.user import User
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
        user: User
        try:
            user = self.user_repository.get_user_by_email(self.session_data.email)
        except Exception:
            raise UserNotFoundError

        if user.password != self.session_data.password:
            raise IncorrectPasswordError
        return SessionSchema.from_model(user)
