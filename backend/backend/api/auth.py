"""Authentication Route Handler
===============================

This module provides handlers for logging in and out as well as refreshing the
JSON Web Token cookie and token.
"""

import falcon
import logzero

from backend.lib.exceptions import InvalidTokenError


def auth_user(username, password):  # pylint: disable=missing-docstring
    return username == 'jo' and password == 'beans'


class AuthHandler(object):
    """Authentication route handlers."""

    def on_get(self, req, res):
        """Validate authentication cookie, issuing a new one and returning a
        new token if valid."""

        token = req.cookies.get('token', '')
        try:
            payload = req.context['decode_token'](token)
            username = payload.get('username')
            if not username:
                raise InvalidTokenError

            new_token = req.context['encode_token']({'username': username})
            res.set_cookie('token', new_token)
            res.media = {'token': new_token}

        except InvalidTokenError:
            logzero.logger.warning('Token Refresh Failed')
            res.set_cookie('token', '')
            raise falcon.HTTPUnauthorized()

    def on_delete(self, req, res):
        """Blank authentication cookie (log user out)."""

        res.set_cookie('token', '')

    def on_post(self, req, res):
        """Validate authentication credentials, issuing a new token and cookie
        if valid."""

        username = req.media.get('username')
        password = req.media.get('password')
        if auth_user(username, password):
            new_token = req.context['encode_token']({'username': username})
            res.set_cookie('token', new_token)
            res.media = {'token': new_token}
        else:
            logzero.logger.warning('Log In Failed')
            raise falcon.HTTPForbidden()
