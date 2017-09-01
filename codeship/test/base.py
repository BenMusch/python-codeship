import unittest
import os


class BaseTest(unittest.TestCase):
    mock_folder = "base"

    def setUp(self):
        self.token = "abcdef"
        self.base_url = "https://api.codeship.com/v2/"

    def load_mock(self, filename):
        cwd = os.path.dirname(__file__)
        mock_file = os.path.join(
                cwd,
                "mocks/%s/%s.json" % (self.mock_folder, filename)
                )
        with open(mock_file, 'r') as f:
            return f.read()
