# -*- coding: utf-8 -*-

from typing_extensions import Protocol

from django.http.request import HttpRequest
from django.http.response import HttpResponse

class ViewFunction(Protocol):
    def __call__(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        ...
