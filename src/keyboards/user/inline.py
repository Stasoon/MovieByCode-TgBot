from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_subscribe_required_markup(channel_usernames):
    markup = InlineKeyboardMarkup(row_width=1)
    
    markup.insert(InlineKeyboardButton('📲 Подписаться 📲', callback_data='subscribe',
                                       url=f'https://t.me/{channel_usernames}'))
    markup.insert(InlineKeyboardButton('✅ Проверить ✅', callback_data='check_sub'))

    return markup




