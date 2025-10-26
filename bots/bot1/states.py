from telebot.handler_backends import State, StatesGroup

class UserStates(StatesGroup):
    name = State()
    phone_or_email = State()
    phone = State()
    email = State()
    message = State()
    checking = State()
    complete = State()