# -*- coding: utf-8 -*-

from typing import ClassVar

from django.conf import ImproperlyConfigured
from django.urls import path
from django.utils.decorators import classonlymethod
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from server.wemake_python_rest.method import Endpoint


class _APIView(View):
    endpoint: ClassVar[Endpoint]

    @classonlymethod
    def as_view(cls, endpoint: Endpoint = None, **kwargs):
        view = super().as_view(**kwargs)
        cls.endpoint = endpoint
        return csrf_exempt(view)

    def dispatch(self, request, *args, **kwargs):
        method_name = request.method.lower()
        method_class = getattr(self.endpoint, method_name, None)
        if method_class is None:
            return self.http_method_not_allowed

        actual_method = method_class(request, *args, **kwargs)
        return actual_method.dispatch()


class Declaration(object):
    def __init__(self) -> None:
        self._endpoints = {}

    def add_endpoint(
        self,
        url: str,
        endpoint: Endpoint,
        name: str,
    ) -> None:
        if url in self._endpoints:
            raise ImproperlyConfigured('Non-unique URL: ' + url)
        self._endpoints[url] = (endpoint, name)

    def urls(self):  # TODO: type List[URLPattern]
        urls_to_include = []

        for url_prefix, endpoint_declaration in self._endpoints.items():
            endpoint, name = endpoint_declaration
            urls_to_include.append(
                # TODO: add option to auto-generate name
                path(url_prefix, _APIView.as_view(endpoint=endpoint), name=name),
            )

        return urls_to_include
