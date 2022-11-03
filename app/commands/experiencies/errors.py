from app.models.errors import BusinessError


class ExperienceNotFoundError(BusinessError):
    def __init__(self):
        msg = "Experience not found"
        super().__init__(msg)


class ExperienceAlreadyExistsError(BusinessError):
    def __init__(self):
        msg = "Experience already exists"
        super().__init__(msg)
