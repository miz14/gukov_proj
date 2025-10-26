from telebot import types
from form.name_handler import get_name_content
from form.states import FormStates
import os

services = [
    'Правовые персональные консультации', 
    'Продукт «Базовый проект»',
    'Продукт «Комплексное проектирование»',
    'Продукт «Корпоративная безопасность»',
    'Продукт «Абонентское обслуживание для блогера»'
]

def get_services_content():
    text = "\n".join([
        '*Мои услуги:*\n',
        f'Полный перечень услуг и цен вы можете найти здесь {os.getenv("SITE2_DOMAIN")}\n\n',

        '*Вы можете выбрать одну из тематик ниже для оставления заявки:*\n',
        *[f'**{i}. {service}**' for i, service in enumerate(services, 1)],
    ])

    markup = types.InlineKeyboardMarkup()
    btns = [types.InlineKeyboardButton(f'Услуга {i}', callback_data=f'service_{i}') for i in range(1, len(services) + 1)]
    markup.add(btns[0])
    markup.add(*btns[1:3])
    markup.add(*btns[3:])
    markup.add(types.InlineKeyboardButton('Главное меню', callback_data='menu'))

    return text, markup

def register_services_handlers(bot):
    
    @bot.callback_query_handler(func=lambda call: call.data == 'services')
    async def callback(call):
        chat_id = call.message.chat.id
        user_id = call.from_user.id

        text, markup = get_services_content()
        await bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown', disable_web_page_preview=True)

        await bot.answer_callback_query(call.id)


    @bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
    async def callback(call):
        i = int(call.data.split('_')[1])
        chat_id = call.message.chat.id
        user_id = call.from_user.id

        async with bot.retrieve_data(user_id, chat_id) as data:
            data['add_service_to_text'] = services[i - 1]
        await bot.set_state(user_id, FormStates.name, chat_id)
        text, markup = get_name_content()
        await bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')

        await bot.answer_callback_query(call.id)
