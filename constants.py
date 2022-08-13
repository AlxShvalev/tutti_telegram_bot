import os
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urljoin

load_dotenv()

BASE_URL = 'https://musopen.org'
SEARCH_URL = urljoin(BASE_URL, '/ru/music/search/?q=')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

DT_FORMAT = '%Y-%m-%d_%H-%M-%S'

LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
LOG_FILE = 'tutti-telegram.log'
LOG_FILE_SIZE = 10 ** 6
BASE_DIR = Path(__file__).parent
