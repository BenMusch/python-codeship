# -*- coding: utf-8 -*-

import pprint
from datetime import datetime

import requests

from .base import BaseAPI


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

    def __init__(self, *args, **kwargs):
        self.expires_at = None
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.organizations = []
        self.access_token = None

    @classmethod
    def create_session(cls, **kwargs):
        email, password = kwargs.get('email'), kwargs.get('password')
        auth = cls(email=email, password=password)
        auth.load()
        return auth

    def load(self):
        basic_auth = requests.auth.HTTPBasicAuth(self.email, self.password)
        data = self._post(self._url(), auth=basic_auth)
        data = self._read_data(data)

        for attr in data.keys():
            setattr(self, attr, data[attr])

        if isinstance(self.expires_at, str) or isinstance(self.expires_at, int):
            self.expires_at = datetime.utcfromtimestamp(self.expires_at)

    def is_active(self):
        return self.expires_at and datetime.utcnow() > self.expires_at
