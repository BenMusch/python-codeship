# -*- coding: utf-8 -*-
import os
import json
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

import requests

from exceptions import *


class BaseAPI(object):
    endpoint = "https://api.codeship.com/v2/"
    namespace = ""

    def __init__(self, *args, **kwargs):
        self.access_token = None
        # handle auth


    def _read_data(self, response):
        if response.status_code == 401:
            raise UnauthorizedError('Incorrect authorization')

        try:
            data = response.json()
        except ValueError as e:
            raise JSONReadError(
                    'Read failed from Codeship: %s' % str(e)
                    )

        if not response.ok:
            msg = data['errors']
            raise BadResponse(msg)
        else:
            return data

    def _post(self, url, **kwargs):
        headers = { 'Content-Type': 'application/json' }
        return requests.post(url, headers=headers, **kwargs)

    def _url(self, path=""):
        return self.endpoint + self.namespace + path

    def __init__(self, *args, **kwargs):
        self.access_token = None

    def __str__(self):
        return "<%s>" % self.__class__.__name__

    def __unicode__(self):
        return u"%s" % self.__str__()

    def __repr__(self):
        return str(self)

