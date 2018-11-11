# -*- coding: utf-8 -*-

from django.urls import path, include

from server.wemake_python_rest.api import Declaration
from server.wemake_python_rest.schemas.views import get_schema_view

from server.main_app.views import UserEndpoint

api = Declaration()
api.add_endpoint(r'user/', UserEndpoint, name='user')

schema_view = get_schema_view(api)  # TODO: provide base path, info, security

urlpatterns = [
    path(r'api/', include(api.urls())),
    path(r'swagger.json', schema_view, name='swagger-json'),
]
