from httpx import HTTPError, HTTPStatusError, ReadTimeout


class AnaplanException(Exception):
    """
    Base class for all Anaplan SDK Exceptions.
    """

    def __init__(self, message: str):
        self.message = message
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


class AnaplanTimeoutException(AnaplanException):
    """
    Exception raised when Anaplan produces a ReadTimeout.
    """

    def __init__(
        self,
        message: str = (
            "Anaplan failed to complete the request within the given timeout. This will often "
            "occur if the model was dormant and needs to loaded first."
        ),
    ):
        self.message = message
        super().__init__(self.message)


def raise_error(error: HTTPError) -> None:
    """
    Raise an appropriate exception based on the error.
    :param error: The error to raise an exception for.
    """
    if isinstance(error, ReadTimeout):
        raise AnaplanTimeoutException from error
    if isinstance(error, HTTPStatusError):
        if error.response.status_code == 404:
            raise InvalidIdentifierException from error
    raise AnaplanException(str(error))
