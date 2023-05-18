from aiogram import types, Dispatcher

from src.utils import mailing
from src.database.user import get_user_ids_to_mailing, get_users_count
from src.database.movie import add_movie_and_get_code, delete_movie_by_code, get_all_movies

commands_explanation_text = ''' 
АДМИНСКИЕ КОМАНДЫ:

/help - вывод справки по всем командам
/users - вывод количества юзеров


Фильмы:
/movies - просмотреть полный список фильмов
<code>/addmovie</code> {текст} {фото} - добавить фильм. Не обязательно: прикрепить фото
<code>/delmovie</code> {число} - удалить фильм по индексу ❗


Рассылка:
/show_post - показывает текущий вид поста
<code>/text</code> {текст} - устанавливает текст рассылки

<code>/photo</code> {фото} - прикрепить фото
/delphoto - удалить фото

<code>/addbttn</code> {ссылка} {текст} - добавляет кнопку
/delbttns - удаляет все кнопки

<code>/mailing</code> - начинает рассылку ‼
'''


async def __handle_help_command(message: types.Message):
    await message.answer(commands_explanation_text)


async def __handle_users_command(message: types.Message):
    await message.answer(f'Всего ботом воспользовались {get_users_count()} человек')


# region Movies

async def __handle_movies_command(message: types.Message):
    output_format = '<code>{0}</code> - {1} \n'
    text = 'Вот список всех фильмов: \n' + ''.join(output_format.format(info[0], info[1]) for info in get_all_movies())
    await message.answer(text, parse_mode='html')


async def __handle_add_movie_command_wout_photo(message: types.Message):
    descr = str(message.get_args())
    if len(descr) > 1:
        movie_code = add_movie_and_get_code(description=descr, )
        await message.answer(f'Фильм добавлен с кодом <code>{movie_code}</code>', parse_mode='html')


async def __handle_add_movie_command_wth_photo(message: types.Message):
    descr = message.caption.split(maxsplit=1)[1]
    if len(descr) > 1:
        movie_code = add_movie_and_get_code(description=descr, photo_file_id=message.photo[0].file_id)
        await message.answer(f'Фильм добавлен с кодом <code>{movie_code}</code>', parse_mode='html')


async def __handle_del_movie_command(message: types.Message):
    args = message.get_args()

    if args.isdigit():
        is_ok = delete_movie_by_code(int(args))
        if is_ok:
            await message.answer('Фильм удалён')
        else:
            await message.answer('Такого фильма нет в базе!')
    else:
        await message.answer('После команды введите код фильма, который хотите удалить')


# endregion


# region Mailing

__mailing_text = 'Привет!'
__mailing_photo_id = None
__mailing_markup = None


async def __start_mailing(message: types.Message):
    user_ids = get_user_ids_to_mailing()
    await mailing.mailing_to_users(message.bot, user_ids, __mailing_text, __mailing_photo_id, __mailing_markup)


async def __show_post(message: types.Message):
    await mailing.mailing_to_users(message.bot, [message.from_id], __mailing_text, __mailing_photo_id, __mailing_markup)


async def __set_mailing_text(message: types.Message):
    global __mailing_text
    __mailing_text = message.html_text.replace('/text ', '')
    await message.answer('Текст установлен')


async def __set_photo(message: types.Message):
    global __mailing_photo_id
    photo = message.photo
    if photo:
        __mailing_photo_id = photo[0].file_id
        await message.answer('Фото установлено')


async def __delete_photo(message: types.Message):
    global __mailing_photo_id
    __mailing_photo_id = None
    await message.answer('Фото удалено')


async def __add_button(message: types.Message):
    global __mailing_markup
    args = message.get_args().split(maxsplit=1)
    bttn = types.InlineKeyboardButton(text=args[1], url=args[0])

    if not __mailing_markup:
        __mailing_markup = types.InlineKeyboardMarkup(row_width=1).insert(bttn)
    else:
        __mailing_markup.insert(bttn)
    await message.answer('Кнопка добавлена!', reply_markup=__mailing_markup)


async def __delete_buttons(message: types.Message):
    global __mailing_markup
    __mailing_markup = None
    await message.answer('Кнопки удалены!')


# endregion


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(__handle_help_command, commands=['help'], is_owner=True)
    dp.register_message_handler(__handle_users_command, commands=['users'], is_owner=True)

    # Фильмы
    dp.register_message_handler(__handle_movies_command, commands=['movies'], is_owner=True)
    dp.register_message_handler(__handle_add_movie_command_wout_photo, commands=['addmovie'], is_owner=True)
    dp.register_message_handler(__handle_add_movie_command_wth_photo, lambda message: '/addmovie' in message.caption,
                                content_types=['photo'], is_owner=True)
    dp.register_message_handler(__handle_del_movie_command, commands=['delmovie'], is_owner=True)

    # Рассылка
    dp.register_message_handler(__start_mailing, commands=['mailing'], is_owner=True)
    dp.register_message_handler(__show_post, commands=['show_post'], is_owner=True)

    dp.register_message_handler(__set_mailing_text, commands=['text'], is_owner=True)
    dp.register_message_handler(__set_photo, lambda message: '/photo' in message.caption, content_types=['photo'],
                                is_owner=True)
    dp.register_message_handler(__delete_photo, commands=['delphoto'], is_owner=True)

    dp.register_message_handler(__add_button, content_types=['text'], commands=['addbttn'], is_owner=True)
    dp.register_message_handler(__delete_buttons, content_types=['text'], commands=['delbttns'], is_owner=True)
