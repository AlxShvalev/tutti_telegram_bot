from aiogram.utils import executor


def main():
    import handlers
    from config import configure_logging, dispatcher

    configure_logging()
    executor.start_polling(dispatcher)


if __name__ == '__main__':
    main()
