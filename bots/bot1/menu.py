from telebot import types

def get_menu_content():
    text = "Здравствйте! Это бот специалиста по пенсионному праву *Гукова Ильи Игоревича*.\nГотов предоставить вам консультацию и помощь в решении пенсионных проблем."

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Услуги', callback_data='services')
    btn2 = types.InlineKeyboardButton('Оставить заявку', callback_data='form')
    markup.add(btn1, btn2)

    return text, markup

def register_menu_handlers(bot):
    @bot.message_handler(commands=['start'])
    
    def start(message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        bot.delete_state(user_id, chat_id)
        text, markup = get_menu_content()
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')

    @bot.callback_query_handler(func=lambda call: call.data == 'menu')
    def callback(call):
        chat_id = call.message.chat.id
        user_id = call.from_user.id
        bot.answer_callback_query(call.id)

        bot.delete_state(user_id, chat_id)
        text, markup = get_menu_content()
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')
