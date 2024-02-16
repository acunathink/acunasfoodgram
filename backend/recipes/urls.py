"""Foodgram recipes URL Configuration.
"""
from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from api.views import APIRecipeCard, FavoriteRecipeViewSet, RecipeViewSet

recipe_router = DefaultRouter()
recipe_router.register(r'', RecipeViewSet, basename='recipes')
recipe_router.register(r'(?P<id>[\d]+)/favorite', FavoriteRecipeViewSet)

urlpatterns = [
    path('<int:id>/shopping_cart/', APIRecipeCard.as_view()),
    path('download_shopping_cart/', APIRecipeCard.as_view()),
    re_path(r'', include(recipe_router.urls)),
]
