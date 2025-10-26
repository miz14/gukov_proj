from telebot import types
from form.states import FormStates

def get_select_phone_or_email_content():
    text = '*Шаг 2. Что вы хотите оставить для обратной связи?*'


    markup = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('Номер телефона', callback_data='form_phone')
    btn2 = types.InlineKeyboardButton('Email', callback_data='form_email')
    cancel_btn = types.InlineKeyboardButton('Отменить', callback_data='cancel_form')

    markup.add(btn1, btn2)
    markup.add(cancel_btn)
    return text, markup