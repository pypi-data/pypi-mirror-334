__all__ = ("ApplicationException",)


class ApplicationException(Exception):
    def __init__(
        self,
        detail: str = "Application exception has occured.",
    ):
        super().__init__(detail)
