import telebot

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = telebot.types.KeyboardButton(text="ИП Дьяченко Алексей Олегович")
button_2 = telebot.types.KeyboardButton(text="ООО Водоресурс")
keyboard.add(button_1, button_2)