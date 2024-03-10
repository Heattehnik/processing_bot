from env import BOT_TOKEN
import telebot
from functions import processing, is_allowed_id, user_reg, user_delete, make_xml, set_protocol_to_1, file_send
from protocol import get_data_for_protocol, make_protocols, make_zip
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
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = telebot.types.KeyboardButton(text="ИП Дьяченко Алексей Олегович")
        button_2 = telebot.types.KeyboardButton(text="ООО Водоресурс")
        keyboard.add(button_1, button_2)
        bot.send_message(message.chat.id, "Выберите организацию", reply_markup=keyboard)
        bot.register_next_step_handler(message, set_organization)


def set_organization(message):
    if message.text:
        bot.send_message(message.chat.id, 'Отправьте файл для обработки', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, processing_file, message.text)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = telebot.types.KeyboardButton(text="ИП Дьяченко Алексей Олегович")
        button_2 = telebot.types.KeyboardButton(text="ООО Водоресурс")
        keyboard.add(button_1, button_2)
        bot.send_message(message.chat.id, 'Выберите организацию', reply_markup=keyboard)
        bot.register_next_step_handler(message, set_organization)


def processing_file(message, organization):
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('temp.xlsx', 'wb') as file:
            file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Ожидайте завершения обработки...')
        check = file_send('temp.xlsx', message.from_user.id, organization, message.chat.id)
        if check.get('errors'):
            reply = []
            errors = check.pop('errors')
            for row, error in errors.items():
                joined_errors = "\n".join(error)
                string = f'{row}:\n {joined_errors}'
                reply.append(string)
            reply = "\n".join(reply)
            row = check['message']
            bot.send_message(message.chat.id, f'{row} \n{reply}')
        else:
            bot.send_message(message.chat.id, 'Обработка завершена!')
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = telebot.types.KeyboardButton(text="ИП Дьяченко Алексей Олегович")
        button_2 = telebot.types.KeyboardButton(text="ООО Водоресурс")
        keyboard.add(button_1, button_2)
        bot.send_message(message.chat.id, 'Выберите организацию', reply_markup=keyboard)
        bot.register_next_step_handler(message, set_organization)
        # xml_ = make_xml(message.chat.id)
        # with open(f'{message.document.file_name[:-5]} ---{xml_[1]}.xml', 'a+') as file:
        #     file.writelines(xml_[0])
        #     file.seek(0)
        #     bot.send_document(message.chat.id, file)
        # os.remove(f'{message.document.file_name[:-5]} ---{xml_[1]}.xml')


@bot.message_handler(commands=['protocol'])
def start_protocol(message):
    if is_allowed_id(message.from_user.id) != message.from_user.id:
        bot.send_message(message.chat.id, 'Извините! Вы не зарегестрированы!')
    else:
        try:
            protocol_list = get_data_for_protocol(message.chat.id)
            bot.send_message(message.chat.id, f"Формирование {len(protocol_list)} протоколов начато...")
            result = make_protocols(protocol_list)
            for item in protocol_list:
                set_protocol_to_1(message.chat.id, item.si_number)
            bot.send_message(message.chat.id, f"Сформировано {result} протоколов. Подготавливается файл к отправке. "
                                              f"Подождите...")
            zip_file = make_zip()

            bot.send_document(message.chat.id, zip_file, visible_file_name='protocols.zip')
            os.remove(f'protocols.zip')
        except Exception as e:
            bot.send_message(message.chat.id, f"{e}")


# @bot.message_handler(commands=['vri_update'])
# def vri_update(message):
#     if is_allowed_id(message.from_user.id) != message.from_user:
#         bot.send_message(message.chat.id, 'Извините! Вы не зарегестрированы!')
#     else:
#         bot.send_message(message.chat.id, 'Введите начальную дату в формате xx.xx.xxxx')
#         bot.register_next_step_handler(message, start_date)
#
#
# def start_date(message):





bot.polling()
