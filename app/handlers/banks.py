from app import bot, States
from app import get_users
from app import Alfa, Tinkoff

from telebot import types


users = get_users()

sessions = {}

@bot.message_handler(func=lambda message: str(message.chat.id) in users.keys(), commands=['banks'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    if message.chat.id not in sessions.keys():
        sessions[message.chat.id] = {}
    try:
        alfa_username = users[str(message.chat.id)]['alfa_login']
        alfa_password = users[str(message.chat.id)]['alfa_pass']
        tinkoff_number = users[str(message.chat.id)]['tinkoff_number']
    except:
        bot.send_message(message.chat.id, "Произошла ошибка при считывании данных для входа\nПроверьте, сохранены ли данные")
        return
        
    sessions[message.chat.id]['alfa'] = Alfa(alfa_username, alfa_password)
    sessions[message.chat.id]['tinkoff'] = Tinkoff(tinkoff_number)
    
    connect_alfa = types.InlineKeyboardButton("Подключиться к Альфа-банку", callback_data='connect_alfa')
    remove_tinkoff = types.InlineKeyboardButton("Подключиться к Тинькофф", callback_data='connect_tinkoff')
    refresh_offers = types.InlineKeyboardButton("Обновить офферы", callback_data='refresh_offers')
    check_connections = types.InlineKeyboardButton("Проверить подключения", callback_data='check_connections')
    markup.add(connect_alfa, remove_tinkoff, refresh_offers, check_connections)

    bot.send_message(message.chat.id, "Что хочешь? \nДля поиска предложений по кэшбеку ответь текстом", reply_markup=markup)
    bot.set_state(message.chat.id, States.banks)



@bot.callback_query_handler(func=lambda call: call.data == 'connect_alfa', state=States.banks)
def send_admin_request(call):
    if sessions[call.message.chat.id]['alfa'].is_connect():
        bot.send_message(call.message.chat.id, "Alfa: Уже подключено")
    else:
        sessions[call.message.chat.id]['alfa'].connect()
        bot.send_message(call.message.chat.id, "Alfa: Введите код")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, alfa_get_code)
    bot.answer_callback_query(call.id)


def alfa_get_code(message):
    text = message.text
    try:
        if sessions[message.chat.id]['alfa'].code(text):
            bot.send_message(message.chat.id, "Alfa: Подключено, запрос офферов")
            try:
                sessions[message.chat.id]['alfa'].response_offers()
                bot.send_message(message.chat.id, "Alfa: Оферы обновлены")
            except:
                bot.send_message(message.chat.id, "Alfa: Ошибка при запросе офферов")
    except:
        bot.send_message(message.chat.id, "Alfa: Ошибка при подключении")





@bot.callback_query_handler(func=lambda call: call.data == 'connect_tinkoff', state=States.banks)
def send_admin_request(call):
    if sessions[call.message.chat.id]['tinkoff'].is_connect():
        bot.send_message(call.message.chat.id, "Tinkoff: Уже подключено")
    else:
        sessions[call.message.chat.id]['tinkoff'].connect()
        bot.send_message(call.message.chat.id, "Tinkoff: Введите код")
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, tinkoff_get_code)
    bot.answer_callback_query(call.id)


def tinkoff_get_code(message):
    text = message.text
    try:
        if sessions[message.chat.id]['tinkoff'].code(text):
            bot.send_message(message.chat.id, "Tinkoff: Подключено, запрос офферов")
            try:
                sessions[message.chat.id]['tinkoff'].response_offers()
                bot.send_message(message.chat.id, "Tinkoff: Оферы обновлены")
            except:
                bot.send_message(message.chat.id, "Tinkoff: Ошибка при запросе офферов")
    except:
        bot.send_message(message.chat.id, "Tinkoff: Ошибка при подключении")

    



@bot.callback_query_handler(func=lambda call: call.data == 'refresh_offers', state=States.banks)
def send_admin_request(call):
    # sessions[call.message.chat.id]['tinkoff'].connect()
    # bot.send_message(call.message.chat.id, "Tinkoff: Введите код")
    try:
        sessions[call.message.chat.id]['alfa'].response_offers()
        bot.send_message(call.message.chat.id, "Alfa: Оферы обновлены")
    except:
        bot.send_message(call.message.chat.id, "Alfa: Ошибка при запросе офферов")

    try:
        sessions[call.message.chat.id]['tinkoff'].response_offers()
        bot.send_message(call.message.chat.id, "Tinkoff: Оферы обновлены")
    except:
        bot.send_message(call.message.chat.id, "Tinkoff: Ошибка при запросе офферов")

    bot.answer_callback_query(call.id)



@bot.callback_query_handler(func=lambda call: call.data == 'check_connections', state=States.banks)
def send_admin_request(call):
    bot.answer_callback_query(call.id)

    try:
        if sessions[call.message.chat.id]['alfa'].is_connect():
            bot.send_message(call.message.chat.id, f"Alfa: Подключено")
        else:
            bot.send_message(call.message.chat.id, f"Alfa: Не подключено")
    except:
        bot.send_message(call.message.chat.id, "Alfa: Ошибка")

    try:
        if sessions[call.message.chat.id]['tinkoff'].is_connect():
            bot.send_message(call.message.chat.id, f"Tinkoff: Подключено")
        else:
            bot.send_message(call.message.chat.id, f"Tinkoff: Не подключено")
    except:
        bot.send_message(call.message.chat.id, "Tinkoff: Ошибка")



@bot.message_handler(func=lambda message: str(message.chat.id) in users.keys(), state=States.banks)
def start(message):
    text = message.text
    try:
        key, val = sessions[message.chat.id]['alfa'].get_near_offers(text)
        bot.send_message(message.chat.id, f"Alfa:\n{key}: {val}")
    except:
        bot.send_message(message.chat.id, "Alfa: Ошибка при запросе офферов")

    try:
        key, val = sessions[message.chat.id]['tinkoff'].get_near_offers(text)
        bot.send_message(message.chat.id, f"Tinkoff:\n{key}: {val}")
    except:
        bot.send_message(message.chat.id, "Tinkoff: Ошибка при запросе офферов")




