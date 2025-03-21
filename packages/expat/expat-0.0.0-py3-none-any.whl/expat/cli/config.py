from expat.config import Config

import click

import logging


logger = logging.getLogger(__name__)


@click.group("config")
def entrypoint():
    pass


@entrypoint.command
@click.pass_obj
def show(config: Config):
    logger.info(
        f"Configuration loaded successfully:\n{config.model_dump_json(indent=4)}\n"
    )
