from telebot import types

async def get_confirm_data_content(bot, user_id, chat_id):
    async with bot.retrieve_data(user_id, chat_id) as data:
        all_form_data = data['all_form_data']
    text = f'<b>Шаг 5. Проверка данных</b>\n\nИмя: {all_form_data['name']}\n{"Email: " + all_form_data['email'] if 'email' in all_form_data else "Телефон: " + all_form_data['phone']}\nТекст заявки: {all_form_data['message']}'
    markup = types.InlineKeyboardMarkup()
    confirm_btn = types.InlineKeyboardButton('Отправить', callback_data='form_finish')
    cancel_btn = types.InlineKeyboardButton('Отменить', callback_data='cancel_form')
    markup.add(cancel_btn, confirm_btn)
    return text, markup