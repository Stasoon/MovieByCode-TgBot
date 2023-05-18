import random


start_sticker_id = 'CAACAgIAAxkBAAEB0PRkY3yAJZVbWY2teJ94jVL_sa2OMAACAQEAAladvQoivp8OuMLmNC8E'
start_video_id = 'CgACAgIAAxkBAAIXRWRkvDcjL4_8nQI_2KbVrcdPw-J9AAL-LAACh7ohS-_UjwZc2s87LwQ'


def get_start_text(first_name: str = 'пользователь') -> str:
    return f'<b>Привет, {first_name}!</b> \n\n' + \
            '🍿 Я помогу тебе найти фильм по коду. \nПросто <i>отправь мне число</i>'


def get_formated_movie_description(description: str = 'Упс, какая-то ошибка 😓') -> str:
    emojis = list('🔥📛🚨💥💯♦🔻🎁🎈')
    description.split()
    return random.choice(emojis) + f" Вот ваш фильм: \n<code>{description}</code>"


def get_movie_was_not_found_text(code: int) -> str:
    return f'Фильм с кодом «<code>{code}</code>» не найден 😓 \n\nПопробуйте позже, фильм скоро будет добавлен 👀'


unexpected_text = 'Я не понимаю 🙈 \n\nОтправь мне код фильма, который хочешь найти 🔎'
