"""JSON Web Token Handler
=========================

A wrapper around the `pyjwt` library that, when used as a falcon middleware,
adds encoding and decoding methods to the request context.
"""

from datetime import datetime

import jwt

from backend.lib.exceptions import InvalidTokenError


class TokenHandler(object):
    """JWT Handler.

    Arguments:
        secret (`str`): Secure session secret for signing keys.
        algorithm (`str`): Hashing algorithm for signing keys.
        duration (`datetime.timedelta`): Expiration window for keys.

    Attributes:
        secret (`str`): Secure session secret for signing keys.
        algorithm (`str`): Hashing algorithm for signing keys.
        duration (`datetime.timedelta`): Expiration window for keys.
    """

    def __init__(self, secret, algorithm, duration):
        self.duration = duration
        self.secret = secret
        self.algorithm = algorithm

    @property
    def claims(self):
        """Creation and expiration claims for JWT payloads."""

        return {
            'nbf': datetime.utcnow(),
            'exp': datetime.utcnow() + self.duration,
        }

    def decode(self, token):
        """Attempt to decode a given JWT.

        Note:
            This method strips creation and expiration claims from the returned
            payload.
        Arguments:
            token (`str`): JWT to decode.
        Returns:
            `dict`: JWT Payload.
        Raises:
            `backend.lib.exceptions.InvalidTokenError`: If the JWT fails
                validation.
        """

        try:
            data = jwt.decode(token, self.secret, self.algorithm)
        except jwt.exceptions.InvalidTokenError:
            raise InvalidTokenError

        return {k: v for k, v in data.items() if k not in self.claims.keys()}

    def encode(self, data):
        """Encode a given payload into a JWT.

        Note:
            This method adds creation and expiration claims to the payload.
        Arguments:
            data (`dict`): The payload to encode.
        Returns:
            `str`: The encoded JWT.
        """

        payload = {**data, **self.claims}
        token = jwt.encode(payload, self.secret, self.algorithm)
        return token.decode()

    def process_request(self, req, res):
        """Falcon middleware request handler to add token handling methods to
        each request."""

        req.context['encode_token'] = self.encode
        req.context['decode_token'] = self.decode
