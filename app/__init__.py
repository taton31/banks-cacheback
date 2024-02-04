import telebot
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters

from telebot.storage import StateMemoryStorage

from dotenv import load_dotenv
load_dotenv('.env')

import os
BOT_TOKEN = os.getenv('BOT_TOKEN')

state_storage = StateMemoryStorage() 

class States(StatesGroup):
    new_user = State() 
    admin = State()
    banks = State()


bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)
from banks_class.alfa_class import Alfa
from banks_class.tinkoff_class import Tinkoff

from db.files import get_admins, save_admins, get_users, save_users, get_request_users, save_request_users


from app.handlers import new_user, admin, config, banks

bot.add_custom_filter(custom_filters.StateFilter(bot))
