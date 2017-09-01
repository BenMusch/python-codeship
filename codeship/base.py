# -*- coding: utf-8 -*-
"""
Base module to handle interactions with the Codeship API
"""
import requests

from .exceptions import JSONReadError, BadResponse, UnauthorizedError


class BaseAPI(object):
    """
    Includes methods to handle interactions with the API

    Subclass BaseAPI to create a new resource
    """
    endpoint = "https://api.codeship.com/v2/"
    namespace = ""

    def __init__(self, *_args, **_kwargs):
        self.access_token = None

    def _read_data(self, response):
        """
        Given a response, parses the data and raises any necessary errors
        """
        if response.status_code == 401:
            raise UnauthorizedError('Incorrect authorization')

        try:
            data = response.json()
        except ValueError as error:
            raise JSONReadError(
                'Read failed from Codeship: %s' % str(error)
                )

        if not response.ok:
            msg = data['errors']
            raise BadResponse(msg)
        else:
            return data

    def _post(self, url, **kwargs):
        """
        Performs a post request
        """
        headers = {'Content-Type': 'application/json'}
        return requests.post(url, headers=headers, **kwargs)

    def _url(self, path=""):
        """
        Generates the url for the current resource

        Define the namespace variable in a class so that _url() is always
        scoped with the namespace
        """
        return self.endpoint + self.namespace + path

    def __str__(self):
        return "<%s>" % self.__class__.__name__

    def __unicode__(self):
        return u"%s" % self.__str__()

    def __repr__(self):
        return str(self)
