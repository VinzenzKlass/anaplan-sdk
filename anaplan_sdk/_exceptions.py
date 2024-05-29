from httpx import HTTPError, HTTPStatusError


class AnaplanException(Exception):
    """
    Base class for all Anaplan SDK Exceptions.
    """

    def __init__(self, message: str):
        self.message = f"\n\n\n{message}\n"
        super().__init__(self.message)


class InvalidCredentialsException(AnaplanException):
    """
    Exception raised when the provided credentials are invalid.
    """

    def __init__(self, message: str = "Invalid credentials."):
        self.message = message
        super().__init__(self.message)


class InvalidPrivateKeyException(InvalidCredentialsException):
    """
    Exception raised when the provided private key is invalid.
    """

    def __init__(self, message: str = "Invalid private key."):
        self.message = message
        super().__init__(self.message)


class InvalidIdentifierException(AnaplanException):
    """
    Exception raised when the provided identifier is invalid.
    """

    def __init__(self, message: str = "Invalid identifier."):
        self.message = message
        super().__init__(self.message)


class AnaplanActionError(AnaplanException):
    """
    Exception raised when an Anaplan Action fails.
    """

    def __init__(self, message: str = "Anaplan completed with errors."):
        self.message = message
        super().__init__(self.message)


def raise_appropriate_error(error: HTTPError) -> None:
    if isinstance(error, HTTPStatusError):
        if error.response.status_code == 404:
            raise InvalidIdentifierException from error
    raise error
