from aiogram import Bot


async def is_subscriber(bot: Bot, channel_username: str | int, user_id: int) -> bool:
    try:
        status = (await bot.get_chat_member('@'+channel_username, user_id)).status
    except Exception as e:
        print(e)
        return False

    if status in ['creator', 'administrator', 'member']:
        return True
    return False
