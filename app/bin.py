import pathlib
import time
from subprocess import call

import click
from alembic.command import revision, upgrade
from alembic.config import Config

ini_path = str(pathlib.Path(__file__).parent / "migrations" / "alembic.ini")
config = Config(ini_path)

# TODO: move all calls to docker into some contextmanager
# or find proper lib to up and down containers


@click.command()
@click.argument("description")
def makemigration(description):
    call(["docker-compose", "up", "-d"])
    time.sleep(2)
    try:
        revision(config, description, True)
        call(["poetry", "run", "pre-commit", "run", "-a"])
    finally:
        call(["docker-compose", "down"])


@click.command()
@click.pass_context
def recreatemigrations(ctx):
    py_files = list(
        (pathlib.Path(__file__).parent / "migrations/versions").glob("*.py")
    )
    if len(py_files) > 1:
        click.echo(
            "You can't recreate initial migration because "
            "you have forward migrations"
        )
    for py_file in py_files:
        py_file.unlink()
    ctx.forward(makemigration, description="Initial migration")


@click.command()
@click.argument("revision", required=False)
def migrate(revision):
    revision = revision or "heads"
    upgrade(config, revision)


@click.command()
@click.pass_context
def server(ctx):
    call(["docker-compose", "up", "-d"])
    time.sleep(2)
    try:
        ctx.forward(migrate)
        call(["poetry", "run", "uvicorn", "app:APP", "--reload"])
    finally:
        call(["docker-compose", "down"])


@click.command()
@click.pass_context
def test(ctx):
    call(["docker-compose", "up", "-d"])
    time.sleep(2)
    try:
        ctx.forward(migrate)
        call(["poetry", "run", "pytest", "-s"])
    finally:
        call(["docker-compose", "down"])


@click.command()
def worker():
    call(
        [
            "poetry",
            "run",
            "celery",
            "-A",
            "app",
            "worker",
            "--loglevel=INFO",
            "--pool=solo",
            "--statedb=celery.db",
        ]
    )
