"""Foodgram api URL Configuration.
"""
from django.urls import include, path, re_path

from rest_framework import routers

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet

api_router = routers.DefaultRouter()
api_router.register(r'tags', TagViewSet)
api_router.register(r'ingredients', IngredientViewSet)
api_router.register(r'recipes', RecipeViewSet)


urlpatterns = [
    path('', include('djoser.urls')),
    re_path(r'', include(api_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
