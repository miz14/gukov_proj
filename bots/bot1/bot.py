import telebot
from telebot.storage import StateRedisStorage
from telebot import custom_filters
from config import BOT_TOKEN

from menu import register_menu_handlers

from form.name import register_name_handlers
from form.phone import register_phone_handlers
from form.email import register_email_handlers
from form.message import register_message_handlers
from form.confirm_data import register_confirm_data_handlers
from form.finish import register_finish_handlers
from form.cancel import register_cancel_handlers

from services import register_services_handlers


state_storage = StateRedisStorage(
    host='localhost', 
    port=6379,
    db=0
)
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))

register_menu_handlers(bot)
register_name_handlers(bot)
register_phone_handlers(bot)
register_email_handlers(bot)
register_message_handlers(bot)
register_confirm_data_handlers(bot)
register_finish_handlers(bot)
register_cancel_handlers(bot)

register_services_handlers(bot)

bot.infinity_polling()