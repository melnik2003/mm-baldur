import sys
import logging

import click
from deepmerge import always_merger

from constants import CONST
from logging_tools import get_logger, setup_logger
from yaml_tools import load_config, ConfigError
from config_validation import validate_cli_params, validate_structure_and_base_config, validate_ops_config
from tools import split_config, prepare_base_config, prepare_ops_config
from file_manager import FileManager


@click.command()
@click.option('--log-level', '-l',
              default=CONST.default_log_level,
              help='Logging level (debug, info, warning, error)')
@click.option('--config-file', '-c',
              default=CONST.default_config_file,
              help='Specify path to config file')
def run(log_level: str, config_file: str) -> None:
    cli_params = {
        'log_level': log_level,
        'config_file': config_file,
    }

    validate_cli_params(cli_params)

    setup_logger(level=log_level)
    logger = get_logger()

    # Load user config
    try:
        user_config: dict = load_config(config_file)
        logger.debug(f'Config {config_file} is loaded')
    except Exception as e:
        logger.error(f'Error loading user config: {e}', exc_info=True)
        sys.exit(1)

    try:
        validate_structure_and_base_config(user_config)
        base_config, ops_config = split_config(user_config)
        validate_ops_config(ops_config)
    except ConfigError as e:
        logger.error(f'Error validating config {config_file}: {e}', exc_info=True)
        sys.exit(1)

    # Merge configs to ensure that all important parameters filled with default values
    # !!! Update logic if more media types supported (such as video and audio)
    base_config = always_merger.merge(CONST.default_base_config_params, base_config)

    # Prepare config
    try:
        prepare_base_config(base_config)
        prepare_ops_config(ops_config) if ops_config else None
    except Exception as e:
        logger.error(f'IE: {e}', exc_info=True)
        sys.exit(1)

    # Process files
    try:
        file_manager = FileManager(base_config, ops_config)
        file_manager.run()
    except Exception as e:
        logger.error(f'{e}', exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    run()
