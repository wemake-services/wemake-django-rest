# -*- coding: utf-8 -*-

import json  # TODO: replace with ujson
from typing import Callable, ClassVar, Generic, TypeVar, Optional

import pavlova
import dataclasses

from django.http import JsonResponse

KT = TypeVar('KT', bound=type)
VT = TypeVar('VT', bound=type)


class Method(Generic[KT, VT]):
    request_payload: ClassVar[KT] = None
    response_payload: ClassVar[VT] = None

    controller: ClassVar[Callable[[Optional[KT]], VT]]

    def dispatch(self, request, *args, **kwargs):  # TODO: rewrite
        # Parse json:
        data = None
        if self.request_payload is not None:
            parser = pavlova.Pavlova()  # TODO: inject parser

            # Load payload:
            data = parser.from_mapping(
                json.loads(request.body),  # TODO: content negotiation
                self.request_payload,
            )

        controller = self.__class__.controller
        response = controller(data)

        # Dumping payload:
        if isinstance(response, list):  # TODO: move to separate class
            response = [dataclasses.asdict(r) for r in response]
        else:
            response = dataclasses.asdict(response)

        # Rendering json:
        return JsonResponse(response, safe=False)
