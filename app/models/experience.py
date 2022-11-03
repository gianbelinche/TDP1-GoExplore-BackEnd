from .errors import ExperienceIncorrectCalendarError


class Experience:
    def __init__(
        self,
        title: str,
        description: str,
        images: list[str],
        preview_image: str,
        calendar: list[dict[str, int]],
        owner: str,
        id: str,
    ):
        self.title = title
        self.description = description
        self.images = images
        self.preview_image = preview_image
        self.calendar = calendar
        self.owner = owner
        self.id = id
