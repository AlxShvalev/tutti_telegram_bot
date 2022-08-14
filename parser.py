import requests
from bs4 import BeautifulSoup as bs
from typing import List, Dict

from utils import find_tag, find_all_tags


def parse_search(response: requests.Response) -> List[Dict[str, str]]:
    """Парсит результаты поиска произведений."""
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


def get_file_data(response: requests.Response) -> Dict[str, str]:
    """Находит информацию по произведению и возвращает её."""
    soup = bs(response.text, features='lxml')
    composer_span = find_tag(soup, 'span', attrs={'itemprop': 'composer'})
    composer = find_tag(composer_span, 'span').text
    title = find_tag(soup, 'h1').text
    a_tag = find_tag(soup, 'a', attrs={'id': 'sheetmusic-download-button'})
    link = a_tag['href']
    return dict(
        composer=composer,
        title=title,
        link=link
    )
