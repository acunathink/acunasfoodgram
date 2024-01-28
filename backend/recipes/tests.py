from http import HTTPStatus

import pytest


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
