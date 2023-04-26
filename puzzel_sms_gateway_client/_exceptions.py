"""Exceptions for the Puzzel SMS Gateway package.

Custom exceptions used by Puzzel SMS Gateway for more helpful error messages.
"""


class PuzzelSmsgwException(Exception):
    """Base class for all exceptions in the Puzzel SMS Gateway package."""


class InvalidDateFormat(PuzzelSmsgwException):
    """Raised when an invalid date format is used."""


class InvalidTimeFormat(PuzzelSmsgwException):
    """Raised when an invalid time format is used."""


class InvalidMsisdnFormat(PuzzelSmsgwException):
    """Raised when an invalid msisdn format is used."""


class InvalidParameter(PuzzelSmsgwException):
    """Raised when an invalid parameter is used."""


class InvalidDcs(PuzzelSmsgwException):
    """Raised when an invalid dcs is used."""


class InvalidUdh(PuzzelSmsgwException):
    """Raised when an invalid udh is used."""


class InvalidPid(PuzzelSmsgwException):
    """Raised when an invalid pid is used."""


class InvalidStrexVerificationTimeout(PuzzelSmsgwException):
    """Raised when an invalid strex verification timeout is used."""


class InvalidStrexConfirmChannel(PuzzelSmsgwException):
    """Raised when an invalid strex confirm channel is used."""


class MissingMessages(PuzzelSmsgwException):
    """Raised when no messages are provided."""


class MissingRecipient(PuzzelSmsgwException):
    """Raised when no recipients are provided."""


class GatewayRequestError(PuzzelSmsgwException):
    """Raised when the request to the gateway fails."""
