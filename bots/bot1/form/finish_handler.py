from telebot import types
from form.states import FormStates
from api import APIService


def get_finish_content():
    text = 'Произошла ошибка при отправке данных, возможно сервис временно не доступен'

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Главное меню', callback_data='menu')
    markup.add(btn)
    return text, markup

def register_finish_handlers(bot):

    @bot.callback_query_handler(func=lambda call: call.data == 'form_finish', state=FormStates.confirm_data)
    async def callback(call):
        chat_id = call.message.chat.id
        user_id = call.from_user.id
        text, markup = get_finish_content()

        async with bot.retrieve_data(user_id, chat_id) as data:
            message = await APIService.send_data(data['all_form_data'], f'@{(await bot.get_me()).username}')
            if message == 'ok':
                text = 'Заявка успешно отправлена'
            elif message == 'uncorrect data':
                text = 'Некорректные данные, повторите попытку'
            data['all_form_data'] = None
            data['add_service_to_text'] = None
        await bot.delete_state(user_id, chat_id)
        await bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')
        await bot.answer_callback_query(call.id)