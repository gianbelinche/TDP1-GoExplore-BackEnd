from typing import List
from app.models.experience import Experience, Location
from app.schemas.experience import (
    ExperienceCreateSchema,
    ExperienceSchema,
    SearchExperience,
)
from .errors import ExperienceAlreadyExistsError, ExperienceNotFoundError
from app.repositories.experience import (
    ExperienceRepository,
    Search,
)
from app.config.logger import setup_logger

logger = setup_logger(__name__)


class CreateExperienceCommand:
    def __init__(
        self,
        experience_repository: ExperienceRepository,
        experience: ExperienceCreateSchema,
    ):
        self.experience_repository = experience_repository
        self.exp_data = experience

    def execute(self) -> ExperienceSchema:
        # experience = ExperienceFactory().create(self.experience_data)
        location = Location(
            description=self.exp_data.location.description,
            lat=self.exp_data.location.lat,
            lng=self.exp_data.location.lng,
        )
        experience = Experience.new(
            title=self.exp_data.title,
            description=self.exp_data.description,
            price=self.exp_data.price,
            score=self.exp_data.score,
            location=location,
            category=self.exp_data.category,
            images=self.exp_data.images,
            preview_image=self.exp_data.preview_image,
            availability=self.exp_data.availability,
            owner=self.exp_data.owner,
        )
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


class SearchExperiencesCommand:
    def __init__(
        self,
        experience_repository: ExperienceRepository,
        search: Search,
    ):
        self.experience_repository = experience_repository
        self.search = search

    def execute(self) -> List[ExperienceSchema]:
        experiences = self.experience_repository.search_experiences(self.search)
        return list(map(ExperienceSchema.from_model, experiences))
