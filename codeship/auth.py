# -*- coding: utf-8 -*-
"""
Handles authentication
"""

from datetime import datetime

import requests

from .base import BaseAPI
from .exceptions import UnauthorizedError


class Auth(BaseAPI):
    """
    Create a session using basic auth:
    https://codeship-api.api-docs.io/v2/authentication/authentication-endpoint

    Args:
        email (string): The email of the codeship user for auth
        password (string): Password for the associated user

    Attributes returned by API:
        access_token (string): The access token for this session
        organizations (list): A list of the organizations and access scopes
        expires_at (int): unix timestamp of expiration
    """
    namespace = "auth/"
    required_attributes = ['password', 'email']

    def __init__(self, *args, **kwargs):
        self.expires_at = None
        self.email = None
        self.password = None
        self.organizations = None
        super(Auth, self).__init__(*args, **kwargs)

    @classmethod
    def create_session(cls, **kwargs):
        """
        Create a new session using basic auth
        Args:
            email
            password
        Return:
            An Auth object
        """
        email, password = kwargs.get('email'), kwargs.get('password')
        auth = cls(email=email, password=password)
        auth.load()
        return auth

    def load(self):
        """
        Performs a request to the auth endpoint to create a new session for the
        given username and password
        """
        basic_auth = requests.auth.HTTPBasicAuth(self.email, self.password)
        data = self._post(self._url(), auth=basic_auth)
        data = self._read_data(data)

        self._set_attrs(**data)

        if isinstance(self.expires_at, (int, str)):
            self.expires_at = datetime.utcfromtimestamp(float(self.expires_at))

    def is_active(self):
        """
        Returns true if the current time is passed the expired_at
        """
        return self.expires_at and datetime.utcnow() > self.expires_at
