import pytest
from django.test.client import Client


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
    client = Client()
    client.force_login(some_one)
    return client
