import os
from telebot.handler_backends import State, StatesGroup

class FormStates(StatesGroup):
    form_name = State()
    form_phone_or_email = State()
    form_phone = State()
    form_email = State()
    form_message = State()
    form_checking = State()
    form_complete = State()

BOT_TOKEN = os.getenv('BOT1_TOKEN')
GOOGLE_POST_URL = os.getenv('GOOGLE_POST_URL')
BOT_SERVICE = 'Юридические услуги в сфере пенсионного права'
