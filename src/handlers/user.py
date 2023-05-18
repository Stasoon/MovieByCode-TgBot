from aiogram import types, Dispatcher

from src.utils import messages, is_subscriber
from src.keyboards.user import inline
from src.create_bot import bot
from src.config import channel_username
from src.database import get_movie_desc_by_code_or_none, create_user


async def __handle_start_command(message: types.Message) -> None:
    create_user(message.from_id, message.from_user.first_name)
    await message.answer_sticker(messages.start_sticker_id)
    await message.answer_animation(caption=messages.get_start_text(message.from_user.first_name), animation=messages.start_video_id)


async def __handle_not_sub_messages(message: types.Message):
    await message.answer('Чтобы начать пользоваться ботом, вы должны быть подписаны:',
                         reply_markup=inline.get_subscribe_required_markup(channel_username))


async def __handle_check_sub_callback(callback: types.CallbackQuery):
    is_sub = await is_subscriber(bot, channel_username, callback.from_user.id)
    if is_sub:
        await callback.message.delete()
        await callback.message.answer('Теперь вы можете пользоваться ботом!')
        await callback.answer()
    else:
       await callback.answer('Вы не подписались!')


async def __handle_code_messages(message: types.Message) -> None:
    await message.answer_chat_action('typing')

    code = int(message.text)
    movie_info = get_movie_desc_by_code_or_none(code)

    if movie_info:
        descript, photo = movie_info[0], movie_info[1]
        if photo:
            await message.answer_photo(caption=messages.get_formated_movie_description(descript), photo=photo)
            return
        await message.answer(messages.get_formated_movie_description(descript))
    else:
        await message.answer(messages.get_movie_was_not_found_text(code))


async def __handle_unexpected_messages(message: types.Message) -> None:
    await message.answer_chat_action('typing')
    await message.answer(messages.unexpected_text)


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__handle_start_command, commands=['start'])
    dp.register_message_handler(__handle_not_sub_messages, content_types=['text'], is_sub=False)
    dp.register_callback_query_handler(__handle_check_sub_callback, text='check_sub')

    dp.register_message_handler(__handle_code_messages, lambda message: message.text.isdigit(), content_types=['text'])
    dp.register_message_handler(__handle_unexpected_messages, content_types=['any'])

