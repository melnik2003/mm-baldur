from pathlib import Path


def validate_file(field, value, error):
    file_path = Path(value)
    if not file_path.is_file():
        error(field, f'{file_path} is not a valid file path')

def validate_dir(field, value, error):
    dir_path = Path(value)
    if not dir_path.is_dir():
        error(field, f'{dir_path} is not a valid directory path')

def validate_new_dir(field, value, error):
    new_dir_path = Path(value)
    try:
        logs_dir = Path(value)
        logs_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        error(field, f'Can\'t use {new_dir_path} path to create a directory: {e}')
