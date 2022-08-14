import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup
from urllib.parse import urljoin

from config import configure_logging
from constants import BASE_URL, SEARCH_URL, TELEGRAM_TOKEN
from parser import parse_search, get_file_data
from utils import get_response, get_download_messgae, get_keyboard

bot = Bot(token=TELEGRAM_TOKEN)

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
    session = requests.Session()
    url = SEARCH_URL + msg.text
    response = get_response(session, url)
    if response is None:
        await bot.send_message(msg.from_user.id, 'Слишком много запросов. '
                                                 'Попробуйте позже.')
    search_list = parse_search(response)
    text, keyboard = get_keyboard(search_list)
    inline_kb = InlineKeyboardMarkup(row_width=1)
    inline_kb.add(*keyboard)

    await bot.send_message(msg.from_user.id, text, reply_markup=inline_kb)


@dispatcher.callback_query_handler()
async def button_callback_handler(call: types.CallbackQuery):
    """Обработчик нажатия инлайн кнопок"""
    url = urljoin(BASE_URL, '/ru/music/', allow_fragments=True)
    url = urljoin(url, call.data)
    session = requests.Session()
    response = get_response(session, url)
    if response is None:
        await bot.send_message(call.from_user.id, 'Слишком много запросов. '
                                                  'Попробуйте позже.')
    file_data = get_file_data(response)
    text = get_download_messgae(file_data)
    await bot.send_message(chat_id=call.from_user.id,
                           text=text,
                           parse_mode='HTML')


def main():
    configure_logging()
    executor.start_polling(dispatcher)


if __name__ == '__main__':
    main()
