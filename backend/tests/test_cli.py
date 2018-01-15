# pylint: disable=missing-docstring,redefined-outer-name,no-self-use
"""Ensure that the CLI commands execute successfully."""
import subprocess
import pathlib
import unittest.mock

import pytest
from click.testing import CliRunner

from manage import cli


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def sub_runner(monkeypatch):
    runner = unittest.mock.Mock()
    monkeypatch.setattr(subprocess, 'run', runner)
    return runner


class TestCommands:
    """Ensure that the cli commands can be invoked."""

    @pytest.mark.parametrize('command', ['doc', 'test', 'lint', 'run'])
    def test_external_commands(self, command, cli_runner, sub_runner):
        result = cli_runner.invoke(cli, [command])
        assert result.exit_code == 0
        assert sub_runner.call_count >= 1
        assert pathlib.Path(sub_runner.call_args[0][0][0]).exists()

    def test_wipe(self, cli_runner):
        result = cli_runner.invoke(cli, ['wipe'])
        assert result.exit_code == 0
