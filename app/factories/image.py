from app.models.image import Image
from app.schemas.experience import ExperienceCreateSchema
from app.models.errors import ExperienceIncorrectCalendarError
from datetime import timedelta, datetime
import uuid

# TODO: Lo que hace esta clase es mas bien responsabilidad de la clase Experience


class ExperienceFactory:
    def create(self, experience_data: ExperienceCreateSchema) -> Experience:
        if not self._is_valid_calendar(experience_data.calendar):
            raise ExperienceIncorrectCalendarError()
        calendar = self._create_new_calendar(experience_data.calendar)
        id = str(uuid.uuid4()) if not experience_data.id else experience_data.id
        return Experience(
            title=experience_data.title,
            description=experience_data.description,
            images=experience_data.images,
            preview_image=experience_data.preview_image,
            calendar=calendar,
            owner=experience_data.owner,
            id=id,
        )

    def _is_valid_calendar(self, calendar: dict) -> bool:
        return (
            "start_date" in calendar
            and "end_date" in calendar
            and "quota" in calendar
            and len(calendar) == 3
            and calendar["start_date"] <= calendar["end_date"]
            and calendar["quota"] >= 0
        )

    def _create_new_calendar(self, calendar):
        def daterange(date1, date2):
            for n in range(int((date2 - date1).days) + 1):
                yield date1 + timedelta(n)

        start_date = calendar["start_date"]
        end_date = calendar["end_date"]
        quota = calendar["quota"]
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ExperienceIncorrectCalendarError()
        return [
            {"date": dt.strftime('%Y-%m-%d'), "quota": quota}
            for dt in daterange(start_dt, end_dt)
        ]
