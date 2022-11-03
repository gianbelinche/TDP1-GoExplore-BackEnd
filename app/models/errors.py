from app.utils.error import GoExploreError


class BusinessError(GoExploreError):
    def __init__(self, message):
        super().__init__(message)


class ExperienceIncorrectCalendarError(BusinessError):
    def __init__(self):
        msg = "Experience has incorrect calendar"
        super().__init__(msg)
