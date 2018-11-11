# -*- coding: utf-8 -*-

from typing import ClassVar

from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse

from server.wemake_python_rest.api import Declaration
from server.wemake_python_rest.types import ViewFunction
from server.wemake_python_rest.schemas.inspectors import Inspector


class _SchemaView(View):
    declaration: ClassVar[Declaration] = None

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        schema_inspector = Inspector(self.declaration)
        return JsonResponse(schema_inspector.generate_schema())


def get_schema_view(declaration: Declaration) -> ViewFunction:
    return _SchemaView.as_view(declaration=declaration)
