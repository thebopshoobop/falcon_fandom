# pylint: disable=missing-docstring,redefined-outer-name,no-self-use
"""Ensure that the configuration classes are properly configured."""

import os
import logging

import pytest

import backend.config as config


@pytest.fixture
def base():
    return config.Config


@pytest.fixture
def environment():
    return {
        'DATABASE_URL': 'guavas',
        'FEEDFIN_DEV': 'true',
        'FEEDFIN_SECRET': 'pineapples',
        'FEEDFIN_LOGFILE': 'papayas',
        'FEEDFIN_LOGBYTES': '42',
        'FEEDFIN_LOGLEVEL': 'debug',
    }


class TestConfig:
    """Ensure that the config class loads properly."""

    def test_defaults(self, base, monkeypatch):
        monkeypatch.setattr(os, "environ", {})
        instance = base()
        assert instance.database_uri == 'sqlite:///:memory:'
        assert not instance.dev_mode
        assert len(instance.secret_key) > 30 and str(instance.secret_key)
        assert not instance.log_file
        assert instance.log_bytes == 1000000
        assert instance.log_level == logging.ERROR

    def test_overrides(self, base, environment, monkeypatch):
        monkeypatch.setattr(os, "environ", environment)
        instance = base()
        assert instance.database_uri == 'guavas'
        assert instance.dev_mode
        assert instance.secret_key == 'pineapples'
        assert instance.log_file == 'papayas'
        assert instance.log_bytes == 42
        assert instance.log_level == logging.DEBUG
