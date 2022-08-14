import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputFile
from io import BytesIO
from urllib.parse import urljoin

from config import configure_logging
from constants import BASE_URL, SEARCH_URL, TELEGRAM_TOKEN
from parser import parse_search, get_file_data
from utils import get_download_message, get_file, get_keyboard, get_response

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


@dispatcher.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nЯ ищу ноты к музыкальным произведениям. '
                        'Пожалуйста, введи название произведения или '
                        'имя композитора на английском языке.')


@dispatcher.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(
        'Я ищу ноты к музыкальным произведениям. '
        'К сожалению, пока я умею обрабатывать запросы только на '
        'английском языке. Пожалуйста, введи запрос латиницей.'
    )


@dispatcher.message_handler()
async def main_handler(msg: types.Message):
    """Основной обработчик текстовых сообщений"""
    session = bot['session']
    url = SEARCH_URL + msg.text
    response = get_response(session, url)
    if response is None:
        await bot.send_message(msg.from_user.id, 'Слишком много запросов. '
                                                 'Попробуйте позже.')
    search_list = parse_search(response)
    keyboard = await get_keyboard(search_list)
    text = f'Результат поиска:\nНайдено произведений: {len(search_list)}\n'

    await bot.send_message(msg.from_user.id, text, reply_markup=keyboard)


@dispatcher.callback_query_handler()
async def button_callback_handler(call: types.CallbackQuery):
    """Обработчик нажатия инлайн кнопок.
    Отправляет файл в ответ на нажатие кнопки"""
    url = urljoin(BASE_URL, '/ru/music/')
    url = urljoin(url, call.data)
    session = bot['session']
    response = get_response(session, url)
    if response is None:
        await bot.send_message(call.from_user.id, 'Слишком много запросов. '
                                                  'Попробуйте позже.')
    file_data = get_file_data(response)
    filename = file_data.get('title')
    text = await get_download_message(file_data)
    tmp = await get_file(file_data.get('link'), bot=bot)
    tmp_to_bytes = BytesIO(tmp.read())
    file = InputFile(path_or_bytesio=tmp_to_bytes, filename=f'{filename}.pdf')
    await bot.send_document(chat_id=call.from_user.id,
                            document=file, caption=text)


def main():
    configure_logging()
    executor.start_polling(dispatcher)


if __name__ == '__main__':
    main()
