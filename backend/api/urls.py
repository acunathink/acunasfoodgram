"""Foodgram api URL Configuration.
"""
from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import CustomUserViewSet, SubscriberViewSet

api_router = DefaultRouter()
api_router.register(r'tags', TagViewSet)
api_router.register(r'ingredients', IngredientViewSet)
api_router.register(r'recipes', RecipeViewSet)
api_router.register(r'users/subscriptions', SubscriberViewSet)
api_router.register(
    r'users/(?P<author_id>[\d]+)/subscribe', SubscriberViewSet
)
api_router.register(r'users', CustomUserViewSet)


urlpatterns = [
    re_path(r'', include(api_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
