from telebot import types

def get_cancel_content():
    text = 'Заявка отменена'

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Главное меню', callback_data='menu')
    markup.add(btn)
    return text, markup

def register_cancel_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == 'cancel_form')
    async def cancel_form(call):
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        await bot.delete_state(user_id, chat_id)
        async with bot.retrieve_data(user_id, chat_id) as data:
            data['all_form_data'] = None
            data['add_service_to_text'] = None
        text, markup = get_cancel_content()
        await bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')

        await bot.answer_callback_query(call.id)