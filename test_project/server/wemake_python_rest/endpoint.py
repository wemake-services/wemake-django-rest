# -*- coding: utf-8 -*-

from typing import Type

from server.wemake_python_rest.method import Method



class Endpoint(object):
    def __init__(  # TODO: dataclass maybe?
        self,
        get: Type[Method] = None,
        post: Type[Method] = None,
        patch: Type[Method] = None,
        put: Type[Method] = None,
        delete: Type[Method] = None,
    ) -> None:
        """"""
        super().__init__()  # TODO: what next?
        self.get = get
        self.post = post
        self.patch = patch
        self.put = put
        self.delete = delete
