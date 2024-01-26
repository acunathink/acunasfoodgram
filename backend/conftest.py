import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client(db, admin_user):
    token, _ = Token.objects.get_or_create(user=admin_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


@pytest.fixture
def some_one(django_user_model):
    return django_user_model.objects.create(
        email='user@example.com',
        username='string',
        first_name='Вася',
        last_name='Пупкин',
        password='Qwerty123'
    )


@pytest.fixture
def some_one_client(some_one):
    token, _ = Token.objects.get_or_create(user=some_one)
    client = APIClient()
    client.force_login(some_one)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client
