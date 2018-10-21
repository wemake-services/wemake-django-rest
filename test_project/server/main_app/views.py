# -*- coding: utf-8 -*-

import dataclasses
from typing import List

from django.contrib.auth.models import User

from server.wemake_python_rest.endpoint import Endpoint
from server.wemake_python_rest.method import Method


@dataclasses.dataclass
class UserRepresentation(object):
    username: str
    email: str


class UserListMethod(Method):
    queryset = User.objects.all()
    response_payload = List[UserRepresentation]

    controller = lambda _: [UserRepresentation(
        username=u.username,
        email=u.email,
    ) for u in UserListMethod.queryset.all()]


UserEndpoint = Endpoint(get=UserListMethod)
