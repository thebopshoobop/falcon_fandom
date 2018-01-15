# pylint: disable=missing-docstring,redefined-outer-name,no-self-use
"""Ensure the proper functioning of the middleware classes."""

from falcon import testing
import pytest

from backend.server import create_api


@pytest.fixture
def client():
    return testing.TestClient(create_api())


class TestAuth:
    def test_poll(self, client):
        result = client.simulate_get('/auth')
        assert result.status_code == 401
        assert not result.cookies['token'].value

    def test_logout(self, client):
        result = client.simulate_delete('/auth')
        assert result.status_code == 200
        assert not result.cookies['token'].value

    def test_login_fail(self, client):
        result = client.simulate_post('/auth')
        assert result.status_code == 400
        token = result.cookies.get('token')
        assert not token or not token.value
