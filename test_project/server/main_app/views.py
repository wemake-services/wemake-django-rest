# -*- coding: utf-8 -*-

import dataclasses
from typing import List

from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from server.wemake_python_rest.controller import BaseController
from server.wemake_python_rest.method import (
    BodylessMethod,
    Endpoint,
    PayloadMethod,
)


@dataclasses.dataclass
class UserRepresentation(object):
    username: str
    email: str


@dataclasses.dataclass
class UserRegistration(UserRepresentation):
    password: str


class _UserListController(BaseController):
    def __call__(self) -> List[UserRepresentation]:
        return [UserRepresentation(
            username=u.username,
            email=u.email,
        ) for u in User.objects.all()]


class UserListMethod(BodylessMethod):
    """Lists all users."""

    response_payload = List[UserRepresentation]
    controller = _UserListController


class _UserCreateController(BaseController):
    def __call__(self, payload: UserRegistration) -> UserRepresentation:
        user = User.objects.create_user(
            username=payload.username,
            email=payload.email,
            password=payload.password,
        )

        return UserRepresentation(
            username=user.username,
            email=user.email,
        )


class UserCreateMethod(PayloadMethod):
    """Creates user."""

    # TODO: response headers, response status code
    response_payload = UserRepresentation
    request_payload = UserRegistration

    controller = _UserCreateController

UserEndpoint = Endpoint(get=UserListMethod, post=UserCreateMethod)
