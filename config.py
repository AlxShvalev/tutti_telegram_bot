import logging
from logging.handlers import RotatingFileHandler

from constants import BASE_DIR, DT_FORMAT, LOG_FILE, LOG_FILE_SIZE, LOG_FORMAT


def configure_logging() -> None:
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / LOG_FILE
    rotation_handler = RotatingFileHandler(
        log_file, maxBytes=LOG_FILE_SIZE, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotation_handler,)
    )
