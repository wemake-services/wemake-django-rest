# -*- coding: utf-8 -*-

import inspect
from dataclasses import fields
from typing import List

from apispec import APISpec
from apispec.utils import validate_spec


class Inspector(object):  # TODO: type everything
    def __init__(self, declaration) -> None:
        self.declaration = declaration
        self.spec = APISpec(  # TODO: user must provide this information
            title='Gisty',
            version='1.0.0',
            openapi_version='2.0',
            info={
                'description': 'A minimal gist API',
            },
        )

    def _operation_internals(self, operation):
        payload_name = operation.response_payload
        if issubclass(operation.response_payload, list):
            payload_name = payload_name.__args__[0]  # TODO: handle list
        else:
            payload_name = operation.response_payload

        # TODO: create separate handlers for list and regular items
        payload_name = payload_name.__qualname__
        if payload_name not in self.spec._definitions:
            self.spec.definition(payload_name, properties={
                'id': {'type': 'integer', 'format': 'int64'},
                'name': {'type': 'string'},
            })

        return {  # TODO: provide other information, not just `responses`
            'responses': {
                200: {  # TODO: status code
                    'description': inspect.getdoc(operation),
                    'schema': {  # TODO: handle list
                        '$ref': '#/definitions/' + payload_name,
                    },
                },
            },
        }

    def _operations_from_endpoint(self, endpoint):
        # TODO: sync names: operation, methods, endpoints, etc
        methods = [method.name for method in fields(endpoint)]
        existing_operations = {}
        for method_name in methods:
            method_declaration = getattr(endpoint, method_name, None)
            if method_declaration is not None:
                existing_operations[method_name] = self._operation_internals(
                    method_declaration,
                )
        return existing_operations

    def generate_schema(self) -> dict:
        endpoints = self.declaration.endpoints
        for url_prefix, endpoint_declaration in endpoints.items():
            endpoint, name = endpoint_declaration
            self.spec.add_path(
                path='/' + url_prefix,  # TODO: normalize url
                operations=self._operations_from_endpoint(endpoint),
            )

        validate_spec(self.spec)
        return self.spec.to_dict()
