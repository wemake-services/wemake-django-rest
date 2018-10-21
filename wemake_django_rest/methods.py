# -*- coding: utf-8 -*-

from collections import defaultdict

from django.urls import path
from django.views import View


class _EndpointView(View):

    @classonlymethod
    def as_view(cls):
        return super().as_view()

class Endpoint(object):
    def __init__(  # TODO: dataclass maybe?
        self,
        get: APIMethod = NotImplemented,
        post: APIMethod = NotImplemented,
        patch: APIMethod = NotImplemented,
        put: APIMethod = NotImplemented,
        delete: APIMethod = NotImplemented,
    ) -> None:
        """"""
        super().__init__()  # TODO: what next?
        self.get = get
        self.post = post
        self.patch = patch
        self.put = put
        self.delete = delete

    def as_view(self):
        def factory(request, *args, **kwargs):
            self.head = getattr(self, 'head', self.get)
            # TODO: do we really need these assignments?
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)
        return factory


class Declaration(object):
    def __init__(self) -> None:
        self._endpoints = {}

    def add_endpoint(
        self,
        url: str,
        endpoint: Endpoint,
        name: str = None,
    ) -> None:
        # TODO: ensure unique url
        self._endpoints[url] = (endpoint, name)

    def urls(self) -> 'List[URLPattern]':  # TODO: type
        urls_to_include = []

        for url_prefix, endpoint_declaraion in self._endpoints.items():
            endpoint, name = endpoint_declaraion
            urls_to_include.append(
                # TODO: add option to auto-generate name
                url(url_prefix, endpoint.as_view(), name=name),
            )
        return urls_to_include


class Method(object):
    pass


class UserListMethod(Method):
    queryset = None
