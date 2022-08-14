import logging
import tempfile

import aiogram
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bs4.element import Tag
from http import HTTPStatus
from requests import RequestException, Response, Session
from typing import Dict, List, Optional


def get_response(session: Session, url: str) -> Response:
    """Устанавливает соединение с переданным url.
    В случае ошибки генерирует исключение."""
    try:
        response = session.get(url=url)
        response.encoding = 'utf-8'
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            return
        return response
    except RequestException:
        logging.exception(f'Возникла ошибка при загрузке страницы {url}')
        raise RequestException(f'Возникла ошибка при загрузке страницы {url}')


def find_tag(soup: Tag, tag: str, attrs: Optional[Dict] = None) -> Tag:
    """Поиск первого тега на странице"""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
    return searched_tag


def find_all_tags(soup: Tag, tag: str, attrs: Optional[Dict] = None) -> list[Tag]:
    """Поиск всех тегов на странице"""
    searched_tags = soup.find_all(tag, attrs=(attrs or {}))
    if searched_tags:
        return searched_tags
    error_msg = f'Не найден тег {tag} {attrs}'
    logging.error(error_msg, stack_info=True)


async def get_keyboard(search_result: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    """Подготовка клавиатуры для результатов поиска"""
    inline_kb = InlineKeyboardMarkup(row_width=1)
    for row in search_result:
        composer = row.get('composer', 'no data')
        title = row.get('title', 'no data')
        link = row.get('link', 'no data')
        link = link.strip().split('/')[-2]
        button = InlineKeyboardButton(
                text=f'{composer}: {title}',
                callback_data=link[:64]
            )
        inline_kb.add(button)

    return inline_kb


async def get_download_message(file_data: dict) -> str:
    """Подготовка сообщения для описания файла"""
    composer = file_data.get('composer', '-no data-')
    title = file_data.get('title', '-no data-')
    text = f'{composer}: {title}'
    return text


async def get_file(url: str, bot: aiogram.Bot) -> tempfile.TemporaryFile:
    """Скачиввет и возвращает файл"""
    session = bot['session']
    response = session.get(url, stream=True)
    if response.status_code == HTTPStatus.OK:
        tmp = tempfile.TemporaryFile()
        tmp.write(response.content)
        tmp.seek(0)
        return tmp
