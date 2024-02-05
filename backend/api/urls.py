"""Foodgram api URL Configuration.
"""
from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from api.views import (APIRecipeCard, IngredientViewSet, RecipeViewSet,
                       TagViewSet)
from users.views import (CustomUserViewSet, SubscriberViewSet,
                         SubscriptionsViewSet)

api_router = DefaultRouter()
api_router.register(r'tags', TagViewSet)
api_router.register(r'ingredients', IngredientViewSet)
api_router.register(r'recipes', RecipeViewSet)
api_router.register(r'users/subscriptions', SubscriptionsViewSet)
api_router.register(
    r'users/(?P<author_id>[\d]+)/subscribe', SubscriberViewSet
)
api_router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('recipes/<int:id>/shopping_cart/', APIRecipeCard.as_view()),
    path('recipes/download_shopping_cart/', APIRecipeCard.as_view()),
    re_path(r'', include(api_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
