"""Foodgram api URL Configuration.
"""
from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers

from api.views import TagViewSet

api_router = routers.DefaultRouter()
api_router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    url(r'', include(api_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
