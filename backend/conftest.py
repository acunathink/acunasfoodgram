import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from recipes.models import Ingredient, Tag


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
def somebody(django_user_model):
    return django_user_model.objects.create(
        email='somebody@example.com',
        username='somebody',
        first_name='Петя',
        last_name='Губкин',
        password='Qwerty123'
    )


@pytest.fixture
def some_one_client(some_one):
    token, _ = Token.objects.get_or_create(user=some_one)
    client = APIClient()
    client.force_login(some_one)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


@pytest.fixture
def tags_create(admin_user):
    Tag.objects.bulk_create(
        [
            Tag(name='Завтрак', color='#010203', slug='breakfast'),
            Tag(name='Обед', color='#112223', slug='lunch'),
            Tag(name='Ужин', color='#312163', slug='dinner')
        ]
    )


@pytest.fixture
def ingredients_create(admin_user):
    Ingredient.objects.bulk_create(
        [
            Ingredient(name='Картошка', measurement_unit='кг'),
            Ingredient(name='Масло', measurement_unit='мл'),
            Ingredient(name='Соль', measurement_unit='г'),
            Ingredient(name='Перец', measurement_unit='г'),
        ]
    )
