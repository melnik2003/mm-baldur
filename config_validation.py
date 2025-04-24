import logging
import sys

from cerberus import Validator

from constants import CONST
from yaml_tools import ConfigError


def validate_cli_params(cli_params):
    v = Validator(CONST.cli_params_schema)
    if not v.validate(cli_params):
        print(f'Invalid CLI parameters: {v.errors}')
        sys.exit(1)

def validate_structure_and_base_config(config):
    """
    Prevalidates structure before splitting the config and the base part all-in-one
    """
    v = Validator(CONST.base_config_schema)
    if v.validate(config):
        logging.debug('Config is valid')
    else:
        logging.error(f'Invalid config: {v.errors}')
        raise ConfigError(f'Invalid config: {v.errors}')

def validate_ops_config(ops_config):
    pass
