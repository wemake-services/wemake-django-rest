# -*- coding: utf-8 -*-

from django.urls import path, include

from server.wemake_python_rest.api import Declaration

from server.main_app.views import UserEndpoint

api = Declaration()
api.add_endpoint(r'user/', UserEndpoint)


urlpatterns = [
    path(r'api/', include(api.urls())),
]
