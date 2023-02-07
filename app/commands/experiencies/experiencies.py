from app.schemas.experience import ExperienceCreateSchema, ExperienceSchema
from .errors import ExperienceAlreadyExistsError, ExperienceNotFoundError
from app.repositories.experience import (
    ExperienceRepository,
)
from app.config.logger import setup_logger
from app.factories.experience import ExperienceFactory

logger = setup_logger(__name__)


class CreateExperienceCommand:
    def __init__(
        self,
        experience_repository: ExperienceRepository,
        experience: ExperienceCreateSchema,
    ):
        self.experience_repository = experience_repository
        self.experience_data = experience

    def execute(self) -> ExperienceSchema:
        experience = ExperienceFactory().create(self.experience_data)
        already_exists = self.experience_repository.experience_exists(experience.id)
        if already_exists:
            raise ExperienceAlreadyExistsError
        experience = self.experience_repository.add_experience(experience)

        return ExperienceSchema.from_model(experience)


class GetExperienceCommand:
    def __init__(self, experience_repository: ExperienceRepository, _id: str):
        self.experience_repository = experience_repository
        self.id = _id

    def execute(self) -> ExperienceSchema:

        exists = self.experience_repository.experience_exists(self.id)
        if not exists:
            raise ExperienceNotFoundError
        experience = self.experience_repository.get_experience(self.id)

        return ExperienceSchema.from_model(experience)
