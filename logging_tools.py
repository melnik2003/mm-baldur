import logging
from datetime import datetime
from pathlib import Path


class ConsoleHandlerNoTraceback(logging.StreamHandler):
    def emit(self, record):
        exc_info = record.exc_info
        record.exc_info = None
        super().emit(record)
        record.exc_info = exc_info

def _generate_log_name() -> str:
    prefix = 'mm'
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f'{prefix}_{timestamp}.log'

def setup_logger(level: str = 'info') -> None:
    logger = logging.getLogger('mm_logger')
    logger.propagate = False

    if logger.hasHandlers():
        return  # Logger is already configured

    logs_dir = Path('logs')
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_path = logs_dir / _generate_log_name()

    level_map = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }
    console_level = level_map.get(level.lower(), logging.INFO)

    logger.setLevel(logging.DEBUG)

    console_handler = ConsoleHandlerNoTraceback()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def get_logger() -> logging.Logger:
    return logging.getLogger('mm_logger')
