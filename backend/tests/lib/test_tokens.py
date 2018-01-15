# pylint: disable=missing-docstring,redefined-outer-name,no-self-use
"""Ensure the security and accuracy of the JWT wrapper."""

from datetime import timedelta
from time import sleep

import pytest

from backend.lib.tokens import TokenHandler
from backend.lib.exceptions import InvalidTokenError


@pytest.fixture
def default():
    return TokenHandler('porpoises', 'HS512', timedelta(1))


@pytest.fixture
def algorithm():
    return TokenHandler('dugongs', 'HS256', timedelta(1))


@pytest.fixture
def secret():
    return TokenHandler('dolphins', 'HS512', timedelta(1))


@pytest.fixture
def timing():
    return TokenHandler('porpoises', 'HS512', timedelta(milliseconds=1))


@pytest.fixture
def user():
    return {'username': 'samantha'}


class TestTokenHandler:
    """Ensure that the JWT wrapper wraps."""

    def test_transcoding(self, default, user):
        token = default.encode(user)
        assert default.decode(token) == user

    def test_algorithm(self, default, algorithm, user):
        default_token = default.encode(user)
        other_token = algorithm.encode(user)

        assert default.decode(default_token) == algorithm.decode(other_token)
        with pytest.raises(InvalidTokenError):
            default.decode(other_token)
        with pytest.raises(InvalidTokenError):
            algorithm.decode(default_token)

    def test_secret(self, default, secret, user):
        default_token = default.encode(user)
        secret_token = secret.encode(user)

        assert default.decode(default_token) == secret.decode(secret_token)
        with pytest.raises(InvalidTokenError):
            default.decode(secret_token)
        with pytest.raises(InvalidTokenError):
            secret.decode(default_token)

    def test_timing(self, timing, user):
        token = timing.encode(user)
        sleep(1)

        with pytest.raises(InvalidTokenError):
            timing.decode(token)
