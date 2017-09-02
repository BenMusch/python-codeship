# -*- coding: utf-8 -*-

from .base import BaseAPI, PRO, BASIC
from .exceptions import IncorrectTypeError


BASIC_ATTRS = (
        "test_pipelines",
        "environment_variables",
        "deployment_pipelines",
        "setup_commands",
        )
PRO_ATTRS = (
        "aes_key"
        )


class Project(BaseAPI):
    namespace = "projects/"
    required_attributes = ["type", "repository_url", "organization_uuid"]

    def __init__(self, *args, **kwargs):
        self.type = kwargs.get('type')
        super(Project, self).__init__(*args, **kwargs)

    def find(self, *args, **kwargs):
        # validate that only org id and project id is there
        pass

    def create(self, *args, **kwargs):
        # validate correct types
        pass

    @classmethod
    def list(cls, *args, **kwargs):
        pass

    def __validate(self):
        super(Project, self).__validate()

        if self.type not in [PRO, BASIC]:
            raise IncorrectTypeError("type must be `pro` or `basic`")

    def __url(self, org_uuid):
        return "{}organizations/{}/{}".format(self.base_url,
                                              self.organization_uuid,
                                              self.namespace)

    def __basic(self):
        return self.type == BASIC

    def __pro(self):
        return self.type == PRO
