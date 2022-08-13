import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup
from urllib.parse import urljoin

from config import configure_logging
from constants import BASE_URL, SEARCH_URL, TELEGRAM_TOKEN
from parser import parse_search, get_notes_url
from utils import get_response, make_message

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
    session = requests.Session()
    url = SEARCH_URL + msg.text
    response = get_response(session, url)
    search_list = parse_search(response)
    text, keyboard = make_message(search_list)
    inline_kb = InlineKeyboardMarkup(row_width=1)
    inline_kb.add(*keyboard)

    await bot.send_message(msg.from_user.id, text, reply_markup=inline_kb)


@dispatcher.callback_query_handler()
async def button_callback_handler(call: types.CallbackQuery):
    url = urljoin(BASE_URL, call.data)
    session = requests.Session()
    response = get_response(session, url)
    file_url = get_notes_url(response)
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'<a href="{file_url}">Скачать файл</a>\n\n',
                           parse_mode='HTML')


def main():
    configure_logging()
    executor.start_polling(dispatcher)


if __name__ == '__main__':
    main()
