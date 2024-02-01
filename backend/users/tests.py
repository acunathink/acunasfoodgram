from http import HTTPStatus

import pytest


@pytest.mark.xfail
@pytest.mark.parametrize(
    'url, expected_status',
    (
        ('/api/users/', HTTPStatus.OK),
        ('/api/users/me/', HTTPStatus.UNAUTHORIZED),
        ('/api/users/1/', HTTPStatus.UNAUTHORIZED),
    ),
)
def test_anon_users_get(db, client, url, expected_status):
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_status',
    (
        ('/api/users/', HTTPStatus.OK),
        ('/api/users/me/', HTTPStatus.OK),
        ('/api/users/1/', HTTPStatus.OK),
    ),
)
@pytest.mark.db
def test_admin_users_get(api_client, url, expected_status):
    response = api_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_status',
    (
        ('/api/users/', HTTPStatus.OK),
        ('/api/users/me/', HTTPStatus.OK),
        ('/api/users/1/', HTTPStatus.OK),
    ),
)
@pytest.mark.db
def test_logged_users_get(some_one_client, url, expected_status):
    response = some_one_client.get(url)
    assert response.status_code == expected_status
