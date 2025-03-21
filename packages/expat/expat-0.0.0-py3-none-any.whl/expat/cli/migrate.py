from expat.config import Config
from expat.db.database import Database

import click

import logging


logger = logging.getLogger(__name__)


@click.group("migrate")
def entrypoint():
    pass


@entrypoint.command
@click.pass_obj
def up(config: Config):
    database = Database.from_config(config)
    database.initialize()


@entrypoint.command
@click.pass_obj
def down(config: Config):
    database = Database.from_config(config)
    database.destroy()
