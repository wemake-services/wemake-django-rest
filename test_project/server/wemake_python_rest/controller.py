# -*- coding: utf-8 -*-

from django.http.request import HttpRequest


class BaseController(object):
    def __init__(self, request: HttpRequest, *args, **kwargs) -> None:
        self.request = request
        self.args = args
        self.kwargs = kwargs
