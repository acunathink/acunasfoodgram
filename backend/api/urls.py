"""Foodgram api URL Configuration.
"""
from django.urls import include, path

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
