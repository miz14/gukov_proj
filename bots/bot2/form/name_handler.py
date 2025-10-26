from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from form.states import FormStates
from form.phone_or_email_handler import get_select_phone_or_email_content
import re

def get_name_content():
    text = '*Шаг 1. Введите ваше имя*'

    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Отменить', callback_data='cancel_form')
    markup.add(btn1)

    return text, markup



def register_name_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == 'form')
    async def callback(call):
        chat_id = call.message.chat.id
        user_id = call.from_user.id

        await bot.set_state(user_id, FormStates.name, chat_id)

        text, markup = get_name_content()
        await bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')

        await bot.answer_callback_query(call.id)

    @bot.message_handler(state=FormStates.name)
    async def form_name(message):
        chat_id = message.chat.id
        user_id = message.from_user.id


        async with bot.retrieve_data(user_id, chat_id) as data:
            if re.match(r'^[A-Za-zА-Яа-я -]{2,}$', message.text) is None:
                await bot.send_message(chat_id, 'Некорректное имя, повторите попытку', parse_mode='markdown')
                return
            data['all_form_data'] = {'name': message.text}

        await bot.set_state(user_id, FormStates.phone_or_email, chat_id)
        next_text, next_markup = get_select_phone_or_email_content()
        await bot.send_message(chat_id, next_text, reply_markup=next_markup, parse_mode='markdown')
