#!/usr/bin/env python
"""
Use `exa --help` to see usage instructions

To make this cli available as an executable on your path, in your root directory type:
```
poetry install
```

Alternatively if using pip, type:
```
pip install -e .
```

Or follow [this guide](https://dbader.org/blog/how-to-make-command-line-commands-with-python).
"""
import subprocess
import sys
from os import system
import click
from django.core import management
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv


application = get_wsgi_application()
load_dotenv()


def run_in_subprocess(command, shell=True, exit_on_error=True):
    # check=True returns 1 for errors, but p.returncode could be 1 or another error code
    p = subprocess.run(command, shell=shell, check=False)

    if exit_on_error and p.returncode != 0:
        sys.exit(p.returncode)


@click.group()
def cli():
    """A command line utility to aid in local development using docker-compose.

    The aim is to save ridiculous amounts of typing cranky commands.

    This utility is intended for running WITHIN a development container.

    Outside the container, you probably want commands like:

        # Open a bash shell in the web container.\n
        docker compose run --rm web bash

        # Build the container for the web service.\n
        docker compose build web

        # Run the basic services that amy web is dependent on.\n
        docker compose up redis db

        # Stop any running containers.\n
        docker compose stop

    """


def _collectstatic(interactive):
    management.call_command("collectstatic", interactive=interactive)


@click.command()
@click.option(
    "--no-input",
    is_flag=True,
    default=False,
    show_default=True,
    help="Do not prompt the user for input",
)
def collectstatic(no_input):
    """Shorthand to run the collectstatic command."""
    interactive = not no_input
    _collectstatic(interactive)


@click.command()
@click.argument("args", nargs=-1)
def makemigrations(args):
    """Shorthand to run the makemigrations command."""
    system(f"python manage.py makemigrations {' '.join(args)}")


@click.command()
@click.argument("args", nargs=-1)
def manage(args):
    """Invoke a django management command.
    `amy manage <args> is shorthand for `python manage.py <args>`
    """
    management.call_command(*args)


def _migrate(args):
    management.call_command("migrate", *args)
    # run_in_subprocess(f"python manage.py migrate {' '.join(args)}")


@click.command()
@click.argument("args", nargs=-1)
def migrate(args):
    """Shorthand to run the migrate command."""
    _migrate(args)


@click.command()
def release():
    """Run all the release commands in one"""
    print("Release step 1: Collect static")
    _collectstatic(interactive=False)

    print("Release step 2: Migrate database")
    _migrate(["--noinput"])


@click.command()
@click.option(
    "--port",
    is_flag=False,
    default="8000",
    show_default=True,
    help="Specify the port to run on",
)
def serve(port):
    """Run the production web server (daphne), no hot reloading."""
    system(f"daphne --proxy-headers -b 0.0.0.0 -p {port} server.asgi:application")


@click.command()
def show_urls():
    """Shorthand to run the show_urls command."""
    management.call_command("show_urls")


@click.command()
@click.argument("addr_port", nargs=1, required=False, default="")
def start(addr_port):
    """Start a hot reloading server for local development.

    Do not use in production (this uses an inefficient and probably insecure server; django's built in runserver).

    `amy start <args>` is shorthand for `python manage.py runserver <args>`

    """
    management.call_command("runserver", addr_port)


cli.add_command(collectstatic)
cli.add_command(makemigrations)
cli.add_command(manage)
cli.add_command(migrate)
cli.add_command(serve)
cli.add_command(show_urls)
cli.add_command(start)
cli.add_command(release)


if __name__ == "__main__":
    cli()
