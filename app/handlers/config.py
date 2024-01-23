from app import bot
from app import get_users, save_users

from telebot import types

users = get_users()

config_opt = {'Альфа: логин': 'config:alfa_login', 'Альфа: пароль': 'config:alfa_pass', 'Тинькофф: номер': 'config:tinkoff_number'}

@bot.message_handler(func=lambda message: str(message.chat.id) in users.keys(), commands=['config'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    for key, value in config_opt.items():
        markup.add(types.InlineKeyboardButton(key, callback_data=value))
    
    bot.delete_state(message.chat.id)
    bot.send_message(message.chat.id, "Здесь можно изменить данные для входа в банки. Что поменяем?", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith('config:') and str(call.message.chat.id) in users.keys())
def send_admin_request(call):

    bot.send_message(call.message.chat.id, 'Введите новое значение')
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, set_config_par, call.data.split(':')[1])
    bot.answer_callback_query(call.id)


def set_config_par(message, par):
    global users
    users = get_users()
    users[str(message.chat.id)][par] = message.text
    save_users(users)
    bot.send_message(message.chat.id, 'Сохранено')
