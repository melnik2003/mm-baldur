import os
import logging
import yaml
from typing import Optional

from logging_tools import get_logger


logger = get_logger()

class ConfigError(Exception):
    """Base class for exceptions related to configuration loading."""
    pass


def load_config(config_path: Optional[str] = None) -> dict:
    if config_path is None:
        config_path = 'default.yaml'

    logger.info(f'Config file: {config_path}')
    logger.debug(f'Loading config file: {config_path}')

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            if config is None:
                raise ConfigError(f'Config file {config_path} is empty')
            return config
    except FileNotFoundError as e:
        raise ConfigError(f'Config file {config_path} not found') from e
    except yaml.YAMLError as e:
        raise ConfigError(f'Error parsing config file {config_path}') from e
    except Exception as e:
        raise




'''
def export_config(config: dict, file_path: str, overwrite: Optional[bool] = False) -> str:
    try:
        # Ensure the output directory exists, if specified
        output_dir = os.path.dirname(file_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logging.info(f"Created directory: {output_dir}")

        # Check if file exists and handle overwrite logic
        if os.path.exists(file_path) and not overwrite:
            logging.error(f"The file '{file_path}' already exists and overwrite is set to False.")
            raise FileExistsError(f"The file '{file_path}' already exists and overwrite is set to False.")

        # Write the dictionary to a YAML file
        with open(file_path, 'w') as yaml_file:
            yaml.safe_dump(config, yaml_file, default_flow_style=False, sort_keys=False)
            logging.info(f"Configuration saved to {file_path}")

        return file_path

    except OSError as e:
        logging.error(f"An error occurred while handling the file '{file_path}'. {e}")
        raise
'''