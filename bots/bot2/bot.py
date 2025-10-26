from telebot.asyncio_storage  import StateRedisStorage
from telebot import asyncio_filters  
from config import BOT_TOKEN
from telebot.async_telebot import AsyncTeleBot
import asyncio

from menu_handler import register_menu_handlers

from form.name_handler import register_name_handlers
from form.phone_handler import register_phone_handlers
from form.email_handler import register_email_handlers
from form.message_handler import register_message_handlers
from form.finish_handler import register_finish_handlers
from form.cancel_handler import register_cancel_handlers

from services_handler import register_services_handlers


state_storage = StateRedisStorage(
    host='localhost', 
    port=6379,
    db=0
)

bot = AsyncTeleBot(BOT_TOKEN, state_storage=state_storage)
bot.add_custom_filter(asyncio_filters.StateFilter(bot))

register_menu_handlers(bot)
register_name_handlers(bot)
register_phone_handlers(bot)
register_email_handlers(bot)
register_message_handlers(bot)
register_finish_handlers(bot)
register_cancel_handlers(bot)

register_services_handlers(bot)

asyncio.run(bot.infinity_polling())