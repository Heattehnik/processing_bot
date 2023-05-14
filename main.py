from env import BOT_TOKEN
import telebot
from functions import processing, make_file, is_allowed_id, user_reg, user_delete, make_xml, set_protocol_to_1
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
        bot.send_message(message.chat.id, "Отправьте файл для обработки")
        bot.register_next_step_handler(message, processing_file)


def processing_file(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('temp.xlsx', 'wb') as file:
        file.write(downloaded_file)
    bot.send_message(message.chat.id, 'Ожидайте завершения обработки...')
    check = processing('temp.xlsx', message.from_user.id)
    if check[2]:
        bot.send_message(message.chat.id, 'Внимание! Обнаружены ранее внесенные счетчики!')
        for item in check[2]:
            bot.send_message(message.chat.id, f'Заводской номер: {item[0]}\n'
                                              f'Дата поверки: {".".join(reversed(item[1][:10].split("-")))}\n'
                                              f'Поверитель: {item[2].title()}')
    if check[0]:
        bot.send_message(message.chat.id, f'Ошибка в строке {check[1] - 1} {check[0]}')
    else:

        bot.send_message(message.chat.id, 'Обработка завершена!')
        xml_ = make_xml(message.chat.id)
        with open(f'{message.document.file_name[:-5]} ---{xml_[1]}.xml', 'a+') as file:
            file.writelines(xml_[0])
            file.seek(0)
            bot.send_document(message.chat.id, file)
        os.remove(f'{message.document.file_name[:-5]} ---{xml_[1]}.xml')


@bot.message_handler(commands=['protocol'])
def start_protocol(message):
    if is_allowed_id(message.from_user.id) != message.from_user.id:
        bot.send_message(message.chat.id, 'Извините! Вы не зарегестрированы!')
    else:
        try:
            bot.send_message(message.chat.id, "Формирование протоколов начато...")
            protocol_list = get_data_for_protocol(message.chat.id)
            result = make_protocols(protocol_list)
            bot.send_message(message.chat.id, f"Сформировано {result} протоколов. Подготавливается файл к отправке. "
                                              f"Подождите...")
            zip_file = make_zip()
            set_protocol_to_1(message.chat.id)
            bot.send_document(message.chat.id, zip_file, visible_file_name='protocols.zip')
            os.remove(f'protocols.zip')
        except Exception as e:
            bot.send_message(message.chat.id, f"{e}")


bot.polling()
