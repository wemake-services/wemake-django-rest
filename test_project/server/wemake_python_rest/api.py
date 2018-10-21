# -*- coding: utf-8 -*-

from typing import ClassVar

from django.urls import path
from django.utils.decorators import classonlymethod
from django.views import View

from server.wemake_python_rest.endpoint import Endpoint


class _APIView(View):
    endpoint: ClassVar[Endpoint]

    @classonlymethod
    def as_view(cls, **kwargs):
        endpoint = kwargs.pop('endpoint')
        view = super().as_view(**kwargs)
        cls.endpoint = endpoint
        return view

    def dispatch(self, request, *args, **kwargs):
        method_name = request.method.lower()
        method_class = getattr(self.endpoint, method_name, None)
        if method_class is None:
            return self.http_method_not_allowed

        actual_method = method_class()
        return actual_method.dispatch(request, *args, **kwargs)


class Declaration(object):
    def __init__(self) -> None:
        self._endpoints = {}

    def add_endpoint(
        self,
        url: str,
        endpoint,  # TODO: type
        name: str = None,
    ) -> None:
        # TODO: ensure unique url
        self._endpoints[url] = (endpoint, name)

    def urls(self):  # TODO: type List[URLPattern]
        urls_to_include = []

        for url_prefix, endpoint_declaration in self._endpoints.items():
            endpoint, name = endpoint_declaration
            urls_to_include.append(
                # TODO: add option to auto-generate name
                path(url_prefix, _APIView.as_view(endpoint=endpoint), name=name),
            )

        print(urls_to_include)
        return urls_to_include
