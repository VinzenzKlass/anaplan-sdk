## AnaplanException

Bases: `Exception`

Base class for all Anaplan SDK Exceptions.

## InvalidCredentialsException

Bases: `AnaplanException`

Exception raised when the provided credentials are invalid.

## InvalidPrivateKeyException

Bases: `InvalidCredentialsException`

Exception raised when the provided private key is invalid.

## InvalidIdentifierException

Bases: `AnaplanException`

Exception raised when the provided identifier is invalid.

## AnaplanActionError

Bases: `AnaplanException`

Exception raised when an Anaplan Action fails.

## AnaplanTimeoutException

Bases: `AnaplanException`

Exception raised when Anaplan produces a Timeout.
