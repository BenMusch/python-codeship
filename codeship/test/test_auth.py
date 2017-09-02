import base64
import unittest
import responses
from datetime import datetime

from ..auth import Auth
from ..exceptions import UnauthorizedError, MissingRequiredParameter

from .base import BaseTest


class TestAuth(BaseTest):
    mock_folder = "auth"

    def setUp(self):
        super(TestAuth, self).setUp()
        self.email = 'test@gmail.com'
        self.password = 'password'
        self.url = self.base_url + "auth/"

    @responses.activate
    def test_valid_auth(self):
        data = self.load_mock("valid")
        responses.add(responses.POST, self.url, body=data, status=200)

        auth_response = Auth.create_session(email=self.email,
                                            password=self.password)
        self.assertEqual(auth_response.access_token,
                         'abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(len(auth_response.organizations), 2)
        self.assertEqual(auth_response.organizations[0],
                {
                'uuid': '11111111-1111-1111-1111-111111111111',
                'scopes': ['project.read', 'build.read']
                })
        self.assertEqual(auth_response.organizations[1],
                {
                'uuid': '22222222-2222-2222-2222-222222222222',
                'scopes': ['project.read', 'project.write', 'build.read', 'build.write']
                })
        self.assertEqual(auth_response.expires_at,
                datetime.utcfromtimestamp(1504291414))

    @responses.activate
    def test_invalid_auth(self):
        responses.add(responses.POST, self.url,
            body=self.load_mock("unauthorized"), status=401)
        with self.assertRaises(UnauthorizedError):
            Auth.create_session(email=self.email, password=self.password)

    @responses.activate
    def test_missing_auth(self):
        with self.assertRaises(MissingRequiredParameter):
            Auth.create_session(email=self.email)

        with self.assertRaises(MissingRequiredParameter):
            Auth.create_session(password=self.password)
