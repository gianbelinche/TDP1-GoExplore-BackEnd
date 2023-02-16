from typing import List, Optional
from app.repositories.config import db
from abc import ABC, abstractmethod
from app.models.experience import Category, Experience, Location
from app.repositories.errors import ExperienceNotFoundError
from datetime import date


class SearchLocation:
    def __init__(self, lat: float, lng: float, dist: int):
        self.lat = lat
        self.lng = lng
        self.dist = dist


class Search:
    def __init__(
        self,
        owner: Optional[str],
        category: Optional[Category],
        location: Optional[SearchLocation],
        limit: int,
    ):
        self.owner = owner
        self.category = category
        self.location = location
        self.limit = limit


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

    @abstractmethod
    def search_experiences(self, search: Search) -> List[Experience]:
        pass

    @abstractmethod
    def get_experiences_by_id(self, ids: List[str]) -> List[Experience]:
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

    def search_experiences(self, search: Search) -> List[Experience]:

        serialized_search = self.__serialize_search(search)
        experiences = self.experiencies.find(serialized_search).limit(search.limit)
        return list(map(self.__deserialize_experience, experiences))

    def get_experiences_by_id(self, ids: List[str]) -> List[Experience]:
        experiences = self.experiencies.find({'_id': {'$in': ids}})
        return list(map(self.__deserialize_experience, experiences))

    def __serialize_search(self, search: Search) -> dict:
        # TODO: location is not being queried
        srch = {
            'owner': search.owner,
            'category': search.category and search.category.value,
        }

        return {k: v for k, v in srch.items() if v is not None}

    def __serialize_experience(self, experience: Experience) -> dict:
        availability = list(map(lambda d: str(d), experience.availability))

        serialized = {
            'title': experience.title,
            'description': experience.description,
            'price': experience.price,
            'score': experience.score,
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
            score=data['score'],
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
