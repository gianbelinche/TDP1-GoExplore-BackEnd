from app.utils.error import GoExploreError


class BusinessError(GoExploreError):
    def __init__(self, message):
        super().__init__(message)
