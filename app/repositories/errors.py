from app.utils.error import GoExploreError


class RepositoryError(GoExploreError):
    def __init__(self, message):
        super().__init__(message)


class UserNotFoundError(RepositoryError):
    def __init__(self):
        msg = "User not found"
        super().__init__(msg)


class ExperienceNotFoundError(RepositoryError):
    def __init__(self):
        msg = "Experience not found"
        super().__init__(msg)


class ImageNotFoundError(RepositoryError):
    def __init__(self):
        msg = "Image not found"
        super().__init__(msg)
