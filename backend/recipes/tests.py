from http import HTTPStatus

import pytest

from recipes.models import Ingredient, Tag


@pytest.mark.parametrize(
    'url, expected_status',
    (
        ('/api/tags/', HTTPStatus.OK),
        ('/api/tags/1/', HTTPStatus.OK),
    ),
)
def test_anon_tags_get(tags_create, client, url, expected_status):
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_status',
    (
        ('/api/tags/', HTTPStatus.OK),
        ('/api/tags/1/', HTTPStatus.OK),
    ),
)
def test_someone_tags_get(tags_create, some_one_client, url, expected_status):
    response = some_one_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_status',
    (
        ('/api/ingredients/', HTTPStatus.OK),
        ('/api/ingredients/1/', HTTPStatus.OK),
    ),
)
def test_ingredients_get(ingredients_create, client, url, expected_status):
    response = client.get(url)
    assert response.status_code == expected_status


def test_tags_create(admin_user):
    Tag.objects.bulk_create(
        [
            Tag(name='Завтрак', color='#010203', slug='breakfast'),
            Tag(name='Обед', color='#112223', slug='lunch'),
            Tag(name='Ужин', color='#312163', slug='dinner')
        ]
    )


def test_ingredients_create(admin_user):
    Ingredient.objects.bulk_create(
        [
            Ingredient(name='Картошка', measurement_unit='кг'),
            Ingredient(name='Масло', measurement_unit='мл'),
            Ingredient(name='Соль', measurement_unit='г'),
            Ingredient(name='Перец', measurement_unit='г'),
        ]
    )
