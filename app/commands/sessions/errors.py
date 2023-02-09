from app.models.errors import BusinessError


class UserNotFoundError(BusinessError):
    def __init__(self):
        msg = "User not found"
        super().__init__(msg)


class IncorrectPasswordError(BusinessError):
    def __init__(self):
        msg = "Incorrect Password"
        super().__init__(msg)
