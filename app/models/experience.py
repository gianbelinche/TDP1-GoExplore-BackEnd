from __future__ import annotations
from datetime import date
from enum import Enum
import uuid


class Location:
    def __init__(self, description: str, lat: float, lng: float):
        self.description = description
        self.lat = lat
        self.lng = lng


class Category(Enum):
    WalkAndRide = "Ride"
    Gastronomy = "Food"
    WellBeing = "Well-being"
    ArtAndCulture = "Art and Culture"
    Sports = "Sports"
    Entertainment = "Entertainment"
    OpenAir = "Outdoors"
    GoingOut = "Going Out"
    Events = "Events"


class Experience:
    def __init__(
        self,
        title: str,
        description: str,
        price: int,
        score: float,
        location: Location,
        category: Category,
        images: list[str],
        preview_image: str,
        availability: list[date],
        owner: str,
        id: str,
    ):
        self.title = title
        self.description = description
        self.price = price
        self.score = score
        self.location = location
        self.category = category
        self.images = images
        self.preview_image = preview_image
        self.availability = availability
        self.owner = owner
        self.id = id

        # TODO: Validate availability[0] < availability[1]

    @classmethod
    def new(
        cls,
        title: str,
        description: str,
        price: int,
        score: float,
        location: Location,
        category: Category,
        images: list[str],
        preview_image: str,
        availability: list[date],
        owner: str,
    ) -> Experience:

        return Experience(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            price=price,
            score=score,
            location=location,
            category=category,
            images=images,
            preview_image=preview_image,
            availability=availability,
            owner=owner,
        )
