from app.repositories.config import db
from abc import ABC, abstractmethod
from app.models.user import User
from app.repositories.errors import UserNotFoundError


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user(self, id: str) -> User:
        pass

    @abstractmethod
    def user_exists(self, id: str) -> bool:
        pass


class PersistentUserRepository(UserRepository):
    def __init__(self):
        COLLECTION_NAME = "Users"
        self.users = db[COLLECTION_NAME]

    def add_user(self, user: User) -> User:
        data = self.__serialize_user(user)
        self.users.insert_one(data)
        return user

    def get_user(self, id: str) -> User:
        user = self.users.find_one({'_id': id})
        if user is None:
            raise UserNotFoundError
        return self.__deserialize_user(user)

    def user_exists(self, id: str) -> bool:
        user = self.users.find_one({'_id': id})
        return user is not None

    def __serialize_user(self, user: User) -> dict:
        serialized = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            '_id': user.id
        }

        return serialized

    def __deserialize_user(
        self,
        data: dict
    ) -> User:

        return User(
            id=data['_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
