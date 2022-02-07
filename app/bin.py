import click
import time
import pathlib

from subprocess import call

# TODO: move all calls to docker into some contextmanager
# or find proper lib to up and down containers


@click.command()
@click.argument("description")
def migrate(description):
    call(["docker-compose", "up", "-d"])
    time.sleep(3)
    try:
        call(
            [
                "poetry",
                "run",
                "alembic",
                "revision",
                "--autogenerate",
                "-m",
                str(description),
            ]
        )
        call(["poetry", "run", "black", "migrations/"])
    finally:
        call(["docker-compose", "down"])


@click.command()
@click.pass_context
def remigrate(ctx):
    py_files = list(pathlib.Path("migrations/versions").glob("*.py"))
    if len(py_files) > 1:
        click.echo(
            "You can't recreate initial migration because "
            "you have forward migrations"
        )
    for py_file in pathlib.Path("migrations/versions").glob("*.py"):
        py_file.unlink()
    ctx.forward(migrate, description="Initial migration")


@click.command()
@click.argument("revision", required=False)
def upgrade(revision):
    revision = revision or "heads"
    call(["poetry", "run", "alembic", "upgrade", str(revision)])


@click.command()
@click.pass_context
def server(ctx):
    call(["docker-compose", "up", "-d"])
    time.sleep(3)
    try:
        ctx.forward(upgrade)
        call(["poetry", "run", "uvicorn", "app.main:app", "--reload"])
    finally:
        call(["docker-compose", "down"])


@click.command()
@click.pass_context
def test(ctx):
    call(["docker-compose", "up", "-d"])
    time.sleep(3)
    try:
        ctx.forward(upgrade)
        call(["poetry", "run", "pytest"])
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
            "app.tasks",
            "worker",
            "--loglevel=INFO",
            "--concurrency=2",
            "--statedb=celery",
        ]
    )
