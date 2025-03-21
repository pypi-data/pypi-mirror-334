from expat.config import Config
from expat.cli import config, migrate

import click

import logging
import os


@click.group
@click.pass_context
@click.option("--config-file", "-c", default=None, type=str)
def entrypoint(context: click.Context, config_file: str | None):
    if config_file is None:
        config_file = os.environ.get("EXPAT_CONFIG_FILE")

        if config_file is None:
            raise ValueError(
                "Config file must be set either via 'EXPAT_CONFIG_FILE' environment "
                "variable or as a command-line argument"
            )

    config = Config(config_file=config_file)  # type: ignore
    context.obj = config

    logging.basicConfig(
        level=config.logs.python_log_level,
        format="%(asctime)s.%(msecs)03d %(levelname)-10s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


entrypoint.add_command(config.entrypoint)
entrypoint.add_command(migrate.entrypoint)
