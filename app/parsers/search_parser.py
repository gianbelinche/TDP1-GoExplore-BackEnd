from app.parsers.errors import LocationIncompleteError
from app.repositories.experience import Search, SearchLocation
from app.schemas.experience import SearchExperience


class SearchExperienceParser:
    def parse(self, search: SearchExperience) -> Search:
        lat, lng = search.lat, search.lng

        if (lat and not lng) or (not lat and lng):
            raise LocationIncompleteError

        location = None
        if lat and lng:
            location = SearchLocation(lat=lat, lng=lng, dist=search.dist)

        return Search(
            location=location,
            owner=search.owner,
            category=search.category,
            limit=search.limit,
        )
