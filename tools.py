from pathlib import Path
import shutil
from constants import CONST


def prepare_base_config(config: dict) -> dict:
    """Normalizes the config for internal usage"""
    # Process every media type
    for media_type, settings in config.items():
        if media_type == 'main':
            continue  # Skip 'main' key

        # Normalize input_exts
        input_exts = settings['input_exts']
        if input_exts == 'all':
            settings['input_exts'] = CONST.supported_types[media_type]
        elif isinstance(input_exts, str):
            settings['input_exts'] = [input_exts]
        elif isinstance(input_exts, list):
            pass  # Skip if input_exts is a list
        else:
            raise ValueError('Config is invalid')

    return config


def prepare_ops_config(config):
    pass


def clean_dir(dir_path: Path) -> None:
    """Cleans the directory by removing all files and subdirectories."""
    # Ensure the path is a directory
    if not dir_path.is_dir():
        raise ValueError(f"{dir_path} is not a valid directory.")

    # Iterate over all items in the directory
    for item in dir_path.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()  # Remove files or symlinks
        elif item.is_dir():
            shutil.rmtree(item)  # Remove subdirectories and their contents


def copy_file(input_path: Path, target_path: Path) -> None:
    shutil.copy(input_path, target_path)


def split_config(full_config):
    """
    Splits config in:
    - base_config: {
        'main': {...},
        'image': {'input_exts': ..., 'output_ext': ...},
        'audio': {'input_exts': ..., 'output_ext': ...},
        'video': {'input_exts': ..., 'output_ext': ...}
      }
    - operations_config: {
        'image': {остальные параметры},
        'audio': {остальные параметры}
        'video': {остальные параметры}
      } or None, if there are no operations
    """
    if 'main' not in full_config:
        raise ValueError("IE: Config must contain 'main' section")

    base_config = {'main': full_config['main'].copy()}
    operations_config = {}

    for section_name, section_config in full_config.items():
        if section_name == 'main':
            continue

        base_config[section_name] = {
            'input_exts': section_config.get('input_exts'),
            'output_ext': section_config.get('output_ext')
        }

        operation_params = {
            k: v for k, v in section_config.items()
            if k not in ('input_exts', 'output_ext')
        }
        if operation_params:
            operations_config[section_name] = operation_params

    return base_config, operations_config or None