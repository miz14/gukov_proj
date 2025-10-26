from telebot import types
from form.states import FormStates
from api import APIService
import asyncio


def get_finish_content():
    text = 'Заявка отправлена'

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Главное меню', callback_data='menu')
    markup.add(btn)
    return text, markup

def register_finish_handlers(bot):

    @bot.callback_query_handler(func=lambda call: call.data == 'form_finish', state=FormStates.finish)
    def callback(call):
        chat_id = call.message.chat.id
        user_id = call.from_user.id
        error = False
        with bot.retrieve_data(user_id, chat_id) as data:
            try:
                asyncio.run(APIService.send_request(data['all_form_data'], f'@{bot.get_me().username}'))
            except:
                error = True
            data['all_form_data'] = None
            data['add_service_to_text'] = None
        bot.delete_state(user_id, chat_id)
        text, markup = get_finish_content()
        if error:
            text = 'Произошла ошибка, возможно сервис временно не доступен'
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')

        bot.answer_callback_query(call.id)