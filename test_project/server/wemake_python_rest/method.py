# -*- coding: utf-8 -*-

import json  # TODO: replace with ujson
from inspect import isfunction
from typing import Callable, ClassVar, Generic, Type, TypeVar, Optional

import pavlova
import dataclasses
from django.http import JsonResponse, HttpResponse, HttpRequest
from typing_extensions import Protocol, final

KT = TypeVar('KT')  # TODO: move to types
VT = TypeVar('VT')  # TODO: rename to RequestPayload, ResponsePayload


class _BodylessController(Protocol[VT]):  # TODO: move to types
    def __init__(self, request, *args, **kwargs) -> None:
        ...

    def __call__(self) -> VT:
        ...


class _PayloadController(Protocol[KT, VT]):  # TODO: move to types
    def __init__(self, request, *args, **kwargs) -> None:
        ...

    def __call__(self, payload: KT) -> VT:
        ...


class _Method(Generic[KT, VT]):
    response_payload: ClassVar[Type[VT]]

    @final
    def __init__(self, request: HttpRequest, *args, **kwargs) -> None:
        self.request = request
        self.args = args
        self.kwargs = kwargs

    @final
    def dispatch(self) -> HttpResponse:
        response = self._call_controller()
        print(response)

        # Dumping payload:
        if isinstance(response, list):  # TODO: move to separate class
            response_body = [dataclasses.asdict(r) for r in response]
            safe = False
        else:
            response_body = dataclasses.asdict(response)
            safe = True

        # TODO: content negotiation
        # Rendering json:
        return JsonResponse(response_body, safe=safe)


class BodylessMethod(_Method):
    controller: ClassVar[_PayloadController]

    @final
    def _call_controller(self) -> VT:
        controller = self.__class__.controller(
            self.request,
            *self.args,
            **self.kwargs,
        )

        return controller()


class PayloadMethod(_Method):
    controller: ClassVar[_PayloadController]
    request_payload: ClassVar[Type[KT]]

    @final
    def _call_controller(self) -> VT:
        # Parse json:
        parser = pavlova.Pavlova()  # TODO: inject parser: self.parser

        # Load payload:
        data = parser.from_mapping(
            json.loads(self.request.body),  # TODO: content negotiation
            self.request_payload,
        )

        controller = self.__class__.controller(
            self.request,
            *self.args,
            **self.kwargs,
        )

        return controller(data)


@dataclasses.dataclass
class Endpoint(object):
    get: Type[_Method] = None
    post: Type[_Method] = None
    patch: Type[_Method] = None
    put: Type[_Method] = None
    delete: Type[_Method] = None
