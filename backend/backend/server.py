"""API Server
=============

This module loads the server configuration, instantiates the API and registers
the route handlers.
"""
import falcon
from logzero import loglevel, logfile, formatter, LogFormatter

from backend.config import Config
from backend.lib.tokens import TokenHandler
from backend.lib.log import LogComponent

from backend.api.auth import AuthHandler
from backend.api.users import UsersHandler


def create_api():
    """Factory function to build a server instance."""

    conf = Config()

    loglevel(conf.log_level)
    logfile(conf.log_file, maxBytes=conf.log_bytes)
    formatter(LogFormatter(fmt=conf.log_format, datefmt=conf.log_date))

    middleware = [
        LogComponent(),
        TokenHandler(conf.secret_key, conf.algorithm, conf.duration)
    ]

    api = falcon.API(middleware=middleware)
    api.resp_options.secure_cookies_by_default = not conf.dev_mode

    api.add_route('/auth', AuthHandler())
    api.add_route('/users', UsersHandler())

    return api
