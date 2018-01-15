"""Users Route Handler
======================

This module provides route handlers for User resources.
"""


import falcon

from backend.lib.auth import auth

USER_FIELDS = ['username', 'password']


class UsersHandler(object):
    """Users route handlers."""

    users = [{'username': 'jo', 'password': 'beans'}]

    def on_get(self, req, res):
        """Return the list of users."""
        res.media = self.users

    @falcon.before(auth)
    def on_post(self, req, res):
        """Add and return a new user."""

        username, password = map(lambda f: req.media.get(f), USER_FIELDS)
        if not username or not password:
            raise falcon.HTTPMissingParam('username or password')

        new_user = {'username': username, 'password': password}
        self.users.append(new_user)
        res.media = new_user
