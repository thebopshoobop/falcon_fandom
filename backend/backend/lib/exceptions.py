"""Exceptions
=============

Custom exception classes for feedfin.
"""


class FeedfinException(Exception):
    """Base feedfin exception."""
    pass


class InvalidTokenError(FeedfinException):
    """Exception for invalid JSON Web Tokens."""
    pass
