import requests
from bs4 import BeautifulSoup as bs
from typing import List, Dict

from utils import find_tag, find_all_tags


def parse_search(response: requests.Response) -> List[Dict[str, str]]:
    """Парсит результаты поиска произведений,
    переходит на страницу каждого произведения"""
    soup = bs(response.text, features='lxml')
    table_rows = find_all_tags(soup, 'div', attrs={'class': 'flex-table-row'})
    result = []

    if table_rows is None:
        return result

    for row in table_rows:
        title_div = find_tag(row, 'div', attrs={'class': 'title'})
        a_tag = find_tag(title_div, 'a')
        title = a_tag.text
        link = a_tag['href']
        composer_div = find_tag(row, 'div', attrs={'class': 'composer'})
        composer = find_tag(composer_div, 'a').text
        data = dict(title=title, composer=composer, link=link)
        result.append(data)

    return result


def get_notes_url(response: requests.Response) -> str:
    """Находит ссылку на файл и возвращает её."""
    soup = bs(response.text, features='lxml')
    a_tag = find_tag(soup, 'a', attrs={'id': 'sheetmusic-download-button'})
    link = a_tag['href']
    return link
