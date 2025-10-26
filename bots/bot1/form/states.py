from telebot.handler_backends import State, StatesGroup

class FormStates(StatesGroup):
    name = State()
    phone_or_email = State()
    phone = State()
    email = State()
    message = State()
    confirm_data = State()
    finish = State()

    cancel = State()
