"""Foodgram api URL Configuration.
"""
from django.urls import include, path, re_path

from rest_framework import routers

from api.views import TagViewSet, ingredientViewSet

api_router = routers.DefaultRouter()
api_router.register(r'tags', TagViewSet)
api_router.register(r'ingredients', ingredientViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    re_path(r'', include(api_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
