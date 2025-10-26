from telebot import types
from form.states import FormStates
from form.confirm_data_handler import get_confirm_data_content

def get_message_content():
    text = '*Шаг 4. Введите ваше сообщение*'

    markup = types.InlineKeyboardMarkup()
    cancel_btn = types.InlineKeyboardButton('Отменить', callback_data='cancel_form')
    markup.add(cancel_btn)
    return text, markup

def register_message_handlers(bot):


    @bot.message_handler(state=FormStates.message)
    async def form_message(message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        form_text = message.text

        async with bot.retrieve_data(user_id, chat_id) as data:
            if data.get('add_service_to_text'):
                form_text = f'Тема: {data["add_service_to_text"]}. {form_text}'
            if len(form_text) > 1000:
                await bot.send_message(chat_id, f'Слишком длинное сообщение, повторите попытку (${len(form_text)}/1000)', parse_mode='markdown')
                return

            data['all_form_data']['message'] = form_text

        await bot.set_state(user_id, FormStates.confirm_data, chat_id)
        next_text, next_markup = await get_confirm_data_content(bot, user_id, chat_id)
        await bot.send_message(chat_id, next_text, reply_markup=next_markup, parse_mode='markdown')