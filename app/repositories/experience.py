from app.repositories.config import db
from abc import ABC, abstractmethod
from app.models.experience import Category, Experience, Location
from app.repositories.errors import ExperienceNotFoundError
from datetime import date


class ExperienceRepository(ABC):
    @abstractmethod
    def add_experience(self, experience: Experience) -> Experience:
        pass

    @abstractmethod
    def get_experience(self, id: str) -> Experience:
        pass

    @abstractmethod
    def experience_exists(self, id: str) -> bool:
        pass


class PersistentExperienceRepository(ExperienceRepository):
    def __init__(self):
        COLLECTION_NAME = "Experiencies"
        self.experiencies = db[COLLECTION_NAME]

    def add_experience(self, experience: Experience) -> Experience:
        data = self.__serialize_experience(experience)
        self.experiencies.insert_one(data)
        return experience

    def get_experience(self, id: str) -> Experience:
        experience = self.experiencies.find_one({'_id': id})
        if experience is None:
            raise ExperienceNotFoundError
        return self.__deserialize_experience(experience)

    def experience_exists(self, id: str) -> bool:
        experience = self.experiencies.find_one({'_id': id})
        return experience is not None

    def __serialize_experience(self, experience: Experience) -> dict:
        availability = list(map(lambda d: str(d), experience.availability))

        serialized = {
            'title': experience.title,
            'description': experience.description,
            'price': experience.price,
            'location': {
                'description': experience.location.description,
                'lat': experience.location.lat,
                'lng': experience.location.lng,
            },
            'category': experience.category.value,
            'images': experience.images,
            'preview_image': experience.preview_image,
            'availability': availability,
            'owner': experience.owner,
            '_id': experience.id,
        }

        return serialized

    def __deserialize_experience(self, data: dict) -> Experience:

        availability = [
            date.fromisoformat(data['availability'][0]),
            date.fromisoformat(data['availability'][1]),
        ]

        return Experience(
            id=data['_id'],
            title=data['title'],
            description=data['description'],
            price=data['price'],
            location=Location(
                description=data['location']['description'],
                lat=data['location']['lat'],
                lng=data['location']['lng'],
            ),
            category=Category(data['category']),
            images=data['images'],
            preview_image=data['preview_image'],
            availability=availability,
            owner=data['owner'],
        )
