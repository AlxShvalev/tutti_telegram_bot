import logging
import requests
from aiogram import Bot, Dispatcher
from logging.handlers import RotatingFileHandler

from constants import (BASE_DIR, DT_FORMAT, LOG_FILE,
                       LOG_FILE_SIZE, LOG_FORMAT, TELEGRAM_TOKEN)


bot = Bot(token=TELEGRAM_TOKEN)
session = requests.Session()
session.headers = {
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://site.ru',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.0 Safari/537.36'
}
bot['session'] = session

dispatcher = Dispatcher(bot)


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
