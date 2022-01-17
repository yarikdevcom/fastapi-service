import click
import time

from subprocess import call


@click.command()
@click.argument("description")
def migrate(description):
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
def test():
    call(["docker-compose", "up", "-d"])
    time.sleep(3)
    try:
        call(["poetry", "run", "pytest"])
    finally:
        call(["docker-compose", "down"])
