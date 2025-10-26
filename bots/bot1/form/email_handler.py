from telebot import types
from form.states import FormStates
import re
from form.message_handler import get_message_content

def get_email_content():
    text = '*Шаг 3. Введите email*'

    markup = types.InlineKeyboardMarkup()
    cancel_btn = types.InlineKeyboardButton('Отменить', callback_data='cancel_form')
    markup.add(cancel_btn)
    return text, markup

def register_email_handlers(bot):

    @bot.callback_query_handler(func=lambda call: call.data == 'form_email', state=FormStates.phone_or_email)
    async def callback(call):
        chat_id = call.message.chat.id
        user_id = call.from_user.id

        await bot.set_state(user_id, FormStates.email, chat_id)
        text, markup = get_email_content()

        await bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')
        await bot.answer_callback_query(call.id)

    @bot.message_handler(state=FormStates.email)
    async def form_email(message):        
        chat_id = message.chat.id
        user_id = message.from_user.id

        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message.text) is None:
            await bot.send_message(chat_id, 'Некорректный email, повторите попытку', parse_mode='markdown')
            return

        async with bot.retrieve_data(user_id, chat_id) as data:
            data['all_form_data']['email'] = message.text

        await bot.set_state(user_id, FormStates.message, chat_id)
        next_text, next_markup = get_message_content()
        await bot.send_message(chat_id, next_text, reply_markup=next_markup, parse_mode='markdown')