from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    'url, expected_status',
    (
        ('/api/users/', HTTPStatus.OK),
        ('/api/users/me/', HTTPStatus.UNAUTHORIZED),
    ),
)
def test_anon_users_get(some_one, client, url, expected_status):
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_status',
    (
        ('/api/users/', HTTPStatus.OK),
        ('/api/users/me/', HTTPStatus.OK),
    ),
)
@pytest.mark.db
def test_logged_users_get(some_one_client, url, expected_status):
    response = some_one_client.get(url)
    assert response.status_code == expected_status
