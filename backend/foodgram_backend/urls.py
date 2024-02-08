"""Foodgram_backend URL Configuration.
"""
from django.contrib import admin
from django.urls import include, path

# handler404 = 'core.views.page_not_found'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
