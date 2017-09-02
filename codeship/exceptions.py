# -*- coding: utf-8 -*-


class JSONReadError(Exception):
    pass


class NotFoundError(Exception):
    pass


class OverLimitError(Exception):
    """
    Raised when the rate limit is exceeded
    https://codeship-api.api-docs.io/v2/introduction/rate-limiting
    """
    pass


class UnauthorizedError(Exception):
    """
    Raised when a user does not have the permissions to access a resource
    https://codeship-api.api-docs.io/v2/authentication/access-and-permissions#permissions
    """
    pass


class SessionExpiredError(Exception):
    """
    Raised when the token is for an expired session
    https://codeship-api.api-docs.io/v2/authentication/authentication-endpoint
    """
    pass


class BadResponse(Exception):
    """
    Handles any non-2x response from the API not handled above
    """
    pass


class IncorectTypeError(Exception):
    """
    Ensures that pro/basic builds/projects are not given attributes for the
    other type
    """


class MissingRequiredParamater(Exception):
    pass
