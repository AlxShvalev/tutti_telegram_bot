import logging
import time

from aiogram.types import InlineKeyboardButton
from bs4.element import Tag
from http import HTTPStatus
from requests import RequestException, Response, Session
from typing import Dict, List, Optional


def get_response(session: Session, url: str) -> Response:
    try:
        response = session.get(url=url)
        response.encoding = 'utf-8'
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            time.sleep(5)
            return get_response(session, url)
        return response
    except RequestException:
        logging.exception(f'Возникла ошибка при загрузке страницы {url}')
        raise RequestException(f'Возникла ошибка при загрузке страницы {url}')


def find_tag(soup: Tag, tag: str, attrs: Optional[Dict] = None) -> Tag:
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
    return searched_tag


def find_all_tags(
        soup: Tag,
        tag: str,
        attrs: Optional[Dict] = None
) -> list[Tag]:
    searched_tags = soup.find_all(tag, attrs=(attrs or {}))
    if searched_tags:
        return searched_tags
    error_msg = f'Не найден тег {tag} {attrs}'
    logging.error(error_msg, stack_info=True)


def make_message(search_result: List[Dict[str, str]]) -> tuple:
    text = 'Результат поиска:\n'
    text += f'Найдено произведений: {len(search_result)}\n'
    keyboard_list = []
    for row in search_result:
        button = InlineKeyboardButton(
                text=(row.get('composer', 'no data') + ': ' +
                      row.get('title', 'no data')),
                callback_data=row.get('link', 'no data')
            )
        keyboard_list.append(button)

    return text, keyboard_list
