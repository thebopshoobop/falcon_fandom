"""Authentication
=================

Function to use with the `falcon.before` decorator to authenticate
requests to the decorated handler.
"""

import falcon
import logzero

from backend.lib.exceptions import InvalidTokenError


def auth(req, *args):
    """For requests to non-excluded paths, validate the JWT in the
    Authorization header.

    Todo:
        * Update from username to slug property
        * Handle authorization as well as authentication
    """

    try:
        payload = req.context['decode_token'](req.auth)
        if not payload.get('username'):
            raise InvalidTokenError

    except InvalidTokenError:
        logzero.logger.warning('Unauthenticated Request')
        raise falcon.HTTPUnauthorized()
