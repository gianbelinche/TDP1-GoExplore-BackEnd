from app.utils.error import GoExploreError


class ParserError(GoExploreError):
    def __init__(self, message):
        super().__init__(message)


class ImageFormatError(ParserError):
    def __init__(self):
        msg = "Invalid image format"
        super().__init__(msg)


class ImageSizeError(ParserError):
    def __init__(self):
        msg = "Image size is too large"
        super().__init__(msg)


class ImageGroupSizeError(ParserError):
    def __init__(self):
        msg = "Image group size is too large"
        super().__init__(msg)


class LocationIncompleteError(ParserError):
    def __init__(self):
        msg = "Location incomplete in search"
        super().__init__(msg)
