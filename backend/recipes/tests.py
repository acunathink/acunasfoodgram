from http import HTTPStatus


def test_subscribe_someone(somebody, some_one_client):
    response2 = some_one_client.get('/api/users/subscriptions/')
    assert response2.status_code == HTTPStatus.OK
