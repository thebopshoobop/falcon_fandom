# pylint: disable=too-few-public-methods,too-many-instance-attributes
"""Configuration
================

This class establishes the configuration settings for running the app. To
override the defaults, you can set the appropriate environment variables.
For ease of development you may store environment variables in a :file:`.env`
file placed in the app hierarchy.

"""

import logging
import warnings
from datetime import timedelta
from secrets import token_urlsafe

from envparse import Env

LOG_MAP = {
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}

# Load environment variables from .env file(s), suppressing the warning if
# there aren't any.
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=UserWarning)
    Env.read_envfile()


class Config(object):
    """Feedfin config class.

    Attributes:
        dev_mode (`bool`): Enable development mode. Defaults to `False`.
            Override with the :envvar:`FEEDFIN_DEV` environment variable.
        secret_key (`str`): Secure session secret. If unset, a new random token
            is generated on app instantiation. Override with the
            :envvar:`FEEDFIN_SECRET` environment variable.
        database_uri (`str`): Database URI for SQLAlchemy. Defaults to
            `sqlite:///:memory:`. Override with the :envvar:`DATABASE_URL`
            environment variable.
        log_file (`str`): File to store log output. Off by default. Override
            with the :envvar:`FEEDFIN_LOGFILE` environment variable.
        log_bytes (`int`): Maximum log file size in bytes. 1000000 by default.
            Override with the :envvar:`FEEDFIN_LOGBYTES` environment variable.
        log_level (`str`): Logging output level. Defaults to error (info in
            debug mode). Override with the :envvar:`FEEDFIN_LOGLEVEL`
            environment variable.
        algorithm (`str`): Hashing algorithm for signing tokens. Set to HS512.
        duration (`timedelta`): Expiration window for tokens. Set to 1 day.
        log_format (`str`): Custom logging format for `logzero`.
        log_date (`str`): Custom log date format for `logzero`.

    Note:
        The `algorithm`, `duration`, `log_format`, and `log_date` settings are
        not currently configurable.
    """

    def __init__(self):
        config = Env(
            DATABASE_URL=dict(default='sqlite:///:memory:'),
            FEEDFIN_DEV=dict(cast=bool, default=False),
            FEEDFIN_SECRET=dict(default=token_urlsafe()),
            FEEDFIN_LOGFILE=dict(default=None),
            FEEDFIN_LOGBYTES=dict(cast=int, default=1000000),
            FEEDFIN_LOGLEVEL=dict(default=None),
        )
        self.database_uri = config('DATABASE_URL')
        self.dev_mode = config('FEEDFIN_DEV')
        self.secret_key = config('FEEDFIN_SECRET')
        self.log_file = config('FEEDFIN_LOGFILE')
        self.log_bytes = config('FEEDFIN_LOGBYTES')
        self.log_level = LOG_MAP.get(config('FEEDFIN_LOGLEVEL'))

        if self.log_level is None:
            self.log_level = logging.INFO if self.dev_mode else logging.ERROR

        # non-configurable
        self.algorithm = 'HS512'
        self.duration = timedelta(1)
        self.log_format = ('%(color)s[%(asctime)s] [feedfin: %(levelname)s]'
                           '%(end_color)s %(message)s')
        self.log_date = '%Y-%m-%d %H:%M:%S'
