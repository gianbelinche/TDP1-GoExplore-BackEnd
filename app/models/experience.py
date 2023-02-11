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
    WalkAndRide = "Paseo"
    Gastronomy = "Gastronomía"
    WellBeing = "Bienestar"
    ArtAndCulture = "Arte y Cultura"
    Sports = "Deportes"
    Entertainment = "Entretenimiento"
    OpenAir = "Aire Libre"


class Experience:
    def __init__(
        self,
        title: str,
        description: str,
        price: int,
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
            location=location,
            category=category,
            images=images,
            preview_image=preview_image,
            availability=availability,
            owner=owner,
        )
