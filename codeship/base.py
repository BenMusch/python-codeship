# -*- coding: utf-8 -*-
"""
Base module to handle interactions with the Codeship API
"""
import requests

from .exceptions import JSONReadError, BadResponse, UnauthorizedError, \
                        MissingRequiredParameter


PRO = 'pro'
BASIC = 'basic'


class BaseAPI(object):
    """
    Includes methods to handle interactions with the API

    Subclass BaseAPI to create a new resource
    """
    endpoint = "https://api.codeship.com/v2/"
    namespace = ""
    requred_attributes = []

    def __init__(self, *_args, **kwargs):
        self.access_token = None
        self._set_attrs(**kwargs)

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
            raise BadResponse(data.get('errors'))
        else:
            return data

    def _post(self, url, **kwargs):
        """
        Performs a post request
        """
        self._check_required_attributes()
        headers = {'Content-Type': 'application/json'}
        return requests.post(url, headers=headers, **kwargs)

    def _url(self, path=""):
        """
        Generates the url for the current resource

        Define the namespace variable in a class so that _url() is always
        scoped with the namespace
        """
        return self.endpoint + self.namespace + path

    def _check_required_attributes(self):
        is_missing = lambda a: not hasattr(self, a) or getattr(self, a) is None
        missing_keys = filter(is_missing, self.required_attributes)

        if missing_keys:
            raise MissingRequiredParameter(
                    'Missing required parameters: {}'.format(
                        ', '.join(missing_keys)
                        )
                    )

    def _validate(self):
        """
        Perform validation before making requests.
        Hook into this method to add custom validations

        Note: This is not used for control flow. You must raise an error to
        perform validation
        """
        self.__check_required_attributes()

    def _set_attrs(self, **kwargs):
        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])

    def __str__(self):
        return "<%s>" % self.__class__.__name__

    def __unicode__(self):
        return u"%s" % self.__str__()

    def __repr__(self):
        return str(self)
