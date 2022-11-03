from .errors import ExperienceIncorrectCalendarError


class Experience:
    def __init__(
        self,
        title: str,
        description: str,
        images: list[str],
        preview_image: str,
        calendar: dict[str, str, int],
        owner: str,
        id: str,
    ):
        if (
            "start_date" not in calendar
            or "end_date" not in calendar
            or "quota" not in calendar
            or len(calendar) != 3
            or calendar["start_date"] > calendar["end_date"]
            or calendar["quota"] < 0
        ):
            raise ExperienceIncorrectCalendarError()
        self.title = title
        self.description = description
        self.images = images
        self.preview_image = preview_image
        self.calendar = calendar
        self.owner = owner
        self.id = id
