from telebot import types
from form.states import FormStates

def get_confirm_data_content(bot, user_id, chat_id):
    with bot.retrieve_data(user_id, chat_id) as data:
        all_form_data = data['all_form_data']
    text = f'*Шаг 5. Проверка данных*\n\nИмя: {all_form_data['name']}\n{"Email: " + all_form_data['email'] if 'email' in all_form_data else "Телефон: " + all_form_data['phone']}\nТекст заявки: {all_form_data['message']}'

    markup = types.InlineKeyboardMarkup()
    confirm_btn = types.InlineKeyboardButton('Отправить', callback_data='form_finish')
    cancel_btn = types.InlineKeyboardButton('Отменить', callback_data='cancel_form')
    markup.add(cancel_btn, confirm_btn)
    return text, markup

def register_confirm_data_handlers(bot):

    @bot.message_handler(state=FormStates.confirm_data)
    def form_confirm_data(message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        bot.set_state(user_id, FormStates.finish, chat_id)
        text, markup = get_confirm_data_content(bot, user_id, chat_id)
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')