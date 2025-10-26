from telebot import types
from form.states import FormStates
import re
from form.message import get_message_content
def get_phone_content():
    text = '*Шаг 3. Введите номер телефона*'

    markup = types.InlineKeyboardMarkup()
    cancel_btn = types.InlineKeyboardButton('Отменить', callback_data='cancel_form')
    markup.add(cancel_btn)
    return text, markup

def register_phone_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == 'form_phone', state=FormStates.phone_or_email)
    def callback(call):
        chat_id = call.message.chat.id
        user_id = call.from_user.id

        bot.set_state(user_id, FormStates.phone, chat_id)
        text, markup = get_phone_content()

        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')
        bot.answer_callback_query(call.id)

    @bot.message_handler(state=FormStates.phone)
    def form_phone(message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        if re.match(r'^\+?[1-9][0-9]{7,14}$', message.text) is None:
            bot.send_message(chat_id, 'Некорректный номер телефона, повторите попытку', parse_mode='markdown')
            return

        with bot.retrieve_data(user_id, chat_id) as data:
            data['all_form_data']['phone'] = message.text

        bot.set_state(user_id, FormStates.message, chat_id)
        next_text, next_markup = get_message_content()
        bot.send_message(chat_id, next_text, reply_markup=next_markup, parse_mode='markdown')