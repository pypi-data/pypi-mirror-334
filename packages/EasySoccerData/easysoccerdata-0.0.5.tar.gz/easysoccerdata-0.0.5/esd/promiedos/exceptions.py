"""
Exceptions for the Promiedos submodule.
"""


class PromiedosException(Exception):
    """
    Base class for Promiedos exceptions.
    """


class InvalidDate(PromiedosException):
    """
    Exception raised when the date is invalid.
    """


class NotMatchIdProvided(PromiedosException):
    """
    Exception raised when no match ID is provided.
    """
