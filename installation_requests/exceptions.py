"""Exceptions."""


class HttpError(Exception):
    """HttpError."""

    error_code = "BAD_REQUEST"
    status_code = 400


class NotFound(HttpError):
    """NotFound Exception."""

    error_code = "NOT_FOUND"
    status_code = 404


class BadRequest(HttpError):
    """BadRequest Exception."""

    error_code = "BAD_REQUEST"
    status_code = 400
