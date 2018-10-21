# -*- coding: utf-8 -*-

"""
Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from server.main_app import urls as main_urls

admin.autodiscover()


urlpatterns = [
    # django-admin:
    path(r'admin/doc/', include('django.contrib.admindocs.urls')),
    path(r'admin/', admin.site.urls),

    # Apps:
    path(r'main/', include(main_urls)),

    # Text and xml static files:
    path(r'robots.txt', TemplateView.as_view(
        template_name='txt/robots.txt',
        content_type='text/plain',
    )),
    path(r'humans.txt', TemplateView.as_view(
        template_name='txt/humans.txt',
        content_type='text/plain',
    )),
]

if settings.DEBUG:  # pragma: no cover
    from django.views.static import serve

    urlpatterns = [
        # Serving media files in development only:
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ] + urlpatterns

# Customize default error views:
# https://docs.djangoproject.com/en/1.11/topics/http/views/#customizing-error-views

# handler400 = 'your_app.views.error_handler'
# handler403 = 'your_app.views.error_handler'
# handler404 = 'your_app.views.error_handler'
# handler500 = 'your_app.views.error_handler'
