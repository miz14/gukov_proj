from telebot import types
from form.name import get_name_content
from form.states import FormStates
import os

services = [
    'Назначение страховой пенсии',
    'Назначение досрочной страховой пенсии',
    'Перерасчет страховой пенсии',
    'Назначение накопительной пенсии или выплаты.',
    'Судебный спор с сфр. ',
    'Запрос архивных справок и документов.'
]

def get_services_content():
    text = "\n".join([
        '*Мои услуги:*\n',
        f'Полный перечень услуг и цен вы можете найти здесь [pensiaigukov.ru]({os.getenv("SITE1_DOMAIN")})\n\n',

        '*Вы можете выбрать одну из тематик ниже для оставления заявки:*\n',
        *[f'**{i}. {service}**' for i, service in enumerate(services, 1)],
    ])

    markup = types.InlineKeyboardMarkup()
    btns = [types.InlineKeyboardButton(f'Услуга {i}', callback_data=f'service_{i}') for i in range(1, len(services) + 1)]
    markup.add(*btns[:3])
    markup.add(*btns[3:])
    markup.add(types.InlineKeyboardButton('Главное меню', callback_data='menu'))

    return text, markup

def register_services_handlers(bot):
    
    @bot.callback_query_handler(func=lambda call: call.data == 'services')
    def callback(call):
        chat_id = call.message.chat.id
        user_id = call.from_user.id

        text, markup = get_services_content()
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')

        bot.answer_callback_query(call.id)


    @bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
    def callback(call):
        i = int(call.data.split('_')[1])
        chat_id = call.message.chat.id
        user_id = call.from_user.id

        with bot.retrieve_data(user_id, chat_id) as data:
            data['add_service_to_text'] = services[i]
            print(data)
        bot.set_state(user_id, FormStates.name, chat_id)
        text, markup = get_name_content()
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='markdown')

        bot.answer_callback_query(call.id)