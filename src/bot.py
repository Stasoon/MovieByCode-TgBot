from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import executor
from src.create_bot import dp, bot

# from bot.middlewares import ThrottlingMiddleware
from src.filters import IsOwnerFilter, IsSubFilter
from src.handlers.reg_handlers import register_all_handlers
from src import database


def __on_startup():
    # создание таблиц в БД
    database.register_models()

    # Регистрация фильтров
    dp.filters_factory.bind(IsOwnerFilter)
    dp.filters_factory.bind(IsSubFilter)

    # регистрация хэндлеров сообщений
    register_all_handlers(dp)

    print('Бот запущен!')


def start_bot():
    executor.start_polling(dp, on_startup=__on_startup(), skip_updates=True)
