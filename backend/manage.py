"""Command line interface
=========================
"""

import subprocess
import pathlib
import sys
import os
from multiprocessing import cpu_count
from secrets import token_urlsafe

import click


# from fin_backend.models import db


def _build_executable(bin_file):
    """Given an executable file name, return a putative path to it in the
    current Python execution context."""

    return pathlib.Path(sys.base_exec_prefix).joinpath(f"bin/{bin_file}")


def _execute(args, env=None):
    """Given a list comprising a shell command and arguments, attempt to run
    the command in a subprocess. If provided an environment dictionary, execute
    the command in a shell populated with that environment."""

    if not pathlib.Path(args[0]).exists():
        click.secho(f"Unable to find {args[0]}.", fg='red', bold=True)
    elif env:
        subprocess.run(' '.join(args), shell=True, env=env)
    else:
        subprocess.run(args)


@click.group()
def cli():
    """This is a management script for the feedfin backend."""


@cli.command()
@click.option('--develop', '-d', envvar='FEEDFIN_DEV', is_flag=True,
              help='Run in development mode.')
@click.option('--port', envvar='FEEDFIN_PORT', default=5000,
              help='Port to serve from.')
@click.option('--host', envvar='FEEDFIN_HOST', default='127.0.0.1',
              help='IP address to bind the server to.')
@click.option('--workers', envvar='FEEDFIN_WORKERS', default=cpu_count() * 2,
              help='Number of Gunicorn worker processes to spawn.')
def run(develop, port, host, workers):
    """Runs the feedfin server."""
    workers = 1 if develop else workers
    options = [f"--bind={host}:{port}",
               f"--workers={workers}", 'backend.app:API']

    if develop:
        options.insert(0, "--reload")
        os.environ['FEEDFIN_DEV'] = 'true'
    elif not os.environ.get('FEEDFIN_SECRET'):
        os.environ['FEEDFIN_SECRET'] = token_urlsafe()

    gunicorn = str(_build_executable('gunicorn'))
    _execute([gunicorn, *options], os.environ)


@cli.command()
def doc():
    """Builds the Sphinx HTML docs."""
    # pylint: disable=no-member
    current = pathlib.Path(__file__).parent.resolve()
    source_dir = current.joinpath('docs/source')
    build_dir = current.joinpath('docs/build')
    sphinx_build = _build_executable('sphinx-build')
    _execute([sphinx_build, source_dir, build_dir])


@cli.command()
def test():
    """Runs the test suite."""
    pytest = _build_executable('pytest')
    _execute([pytest])


@cli.command()
def lint():
    """Runs the linter."""
    pylint = _build_executable('pylint')
    click.secho('Linting App', fg='blue', bold=True)
    _execute([pylint, 'backend'])
    click.secho('Linting Tests', fg='blue', bold=True)
    _execute([pylint, 'tests'])
    click.secho('Linting CLI', fg='blue', bold=True)
    _execute([pylint, 'manage.py'])


@cli.command()
def wipe():
    """Resets the database."""
    # db.drop_all()
    # db.create_all()
    # db.session.commit()  # pylint: disable=no-member


if __name__ == "__main__":
    cli()
