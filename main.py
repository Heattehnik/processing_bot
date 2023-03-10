from env import BOT_TOKEN
import telebot
from functions import processing, make_file, is_allowed_id, user_reg, user_delete
import os

bot = telebot.TeleBot(BOT_TOKEN)

#@bot.message_handler(commands=['userdel'])
#def user_registration(message):
#    user_delete(message.from_user.id)


#@bot.message_handler(commands=['register'])
#def user_registration(message):
#    user_reg(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
#    bot.send_message(message.chat.id, 'Вы зарегестрированы!')

@bot.message_handler(commands=['upload'])
def welcome(message):
    if is_allowed_id(message.from_user.id) != message.from_user.id:
        bot.send_message(message.chat.id, 'Извините! Вы не зарегестрированы!')
    else:
        bot.send_message(message.chat.id, "Отправьте файл для обработки")
        bot.register_next_step_handler(message, processing_file)


def processing_file(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('temp.xlsx', 'wb') as file:
        file.write(downloaded_file)
    bot.send_message(message.chat.id, 'Ожидайте завершения обработки...')
    check = processing('temp.xlsx', message.from_user.id)
    if check[0]:
        bot.send_message(message.chat.id, f'Ошибка в строке {check[1] - 1} {check[0]}')
    else:
        bot.send_message(message.chat.id, 'Обработка завершена!')


# @bot.message_handler(commands=['download'])
# def ask_date(message):
#     if is_allowed_id(message.from_user.id) != message.from_user.id:
#         bot.send_message(message.chat.id, 'Извините! Вы не зарегестрированы!')
#     else:
#         bot.send_message(message.chat.id, "Введите дату поверки для выгрузки.")
#         bot.register_next_step_handler(message, file_preparing)
#
#
# def file_preparing(message):
#     date = message.text
#     splited_date = date.split('.')
#     splited_date.reverse()
#     joined_date = '-'.join(splited_date)
#     file_name = make_file(joined_date)
#     with open(file_name, 'rb') as file:
#         bot.send_document(message.chat.id, file)
#     os.remove(file_name)


bot.polling()
