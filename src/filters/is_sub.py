from aiogram import Bot, types
from aiogram.dispatcher.filters import BoundFilter
from src.config import channel_username


class IsSubFilter(BoundFilter):
    """
    Custom filter "is_sub".
    """
    key = "is_sub"

    def __init__(self, is_sub):
        self.is_sub = is_sub

    async def check(self, message: types.Message):
        try:
            user = await message.bot.get_chat_member('@' + channel_username, message.from_user.id)
        except Exception as e:
            print(e)
            return False

        if user.status not in ['creator', 'administrator', 'member']:
            return True
        return False
