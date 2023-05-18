import asyncio
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils import exceptions


# Рассылка производится по частям для оптимизации
__users_count_in_part = 30
__seconds_btw_parts = 0.5


async def mailing_to_users(bot: Bot, user_ids: list[int] | tuple[int], message_text: str, image_file_id: str = None, inline_kb: None | InlineKeyboardMarkup = None):
    for index, user_id in enumerate(user_ids, start=1):
        try:
            if not image_file_id:
                await bot.send_message(chat_id=user_id, text=message_text, parse_mode='html', reply_markup=inline_kb)
            else:
                await bot.send_photo(chat_id=user_id, photo=image_file_id, caption=message_text, parse_mode='html', reply_markup=inline_kb)
        except exceptions as e:
            print(f'ошибка при отправке рассылки для {user_id}:', e)

        # немного ждём перед отправкой следующих сообщений
        if index % __users_count_in_part == 0:
            await asyncio.sleep(__seconds_btw_parts)
