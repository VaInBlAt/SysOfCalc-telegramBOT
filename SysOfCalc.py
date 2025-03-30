import telebot
from telebot import types

bot = telebot.TeleBot('TOKEN')
first_Encrypt = 10
second_Encrypt = 2
isFirst = True


@bot.message_handler(commands=['start'])
def show_encrypt_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2')
    btn2 = types.KeyboardButton('8')
    btn3 = types.KeyboardButton('10')
    btn4 = types.KeyboardButton('16')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    bot.send_message(message.chat.id, 'Из какой кодировки переводим число?', reply_markup=markup)
    bot.register_next_step_handler(message, set_first_encrypt)


def set_first_encrypt(message):
    global first_Encrypt
    try:
        first_Encrypt = int(message.text)
        show_encrypt_menu_second(message)
    except ValueError:
        global isFirst
        if isFirst == True:
            bot.send_message(message.chat.id, 'Ошибка: Пожалуйста, введите корректное значение (2, 8, 10 или 16).')
            show_encrypt_menu(message)
        isFirst = False


def show_encrypt_menu_second(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2')
    btn2 = types.KeyboardButton('8')
    btn3 = types.KeyboardButton('10')
    btn4 = types.KeyboardButton('16')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    bot.send_message(message.chat.id, 'В какую кодировку переводим число?', reply_markup=markup)
    bot.register_next_step_handler(message, set_second_encrypt)


def set_second_encrypt(message):
    global second_Encrypt
    try:
        second_Encrypt = int(message.text)
        bot.send_message(message.chat.id, f'Переводим из {first_Encrypt} в {second_Encrypt}. Введите число для кодировки.',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, encrypt)
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка: Пожалуйста, введите корректное значение (2, 8, 10 или 16).')
        show_encrypt_menu_second(message)


def encrypt(message):
    incrypt = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
               'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    reverse_incrypt = {v: k for k, v in incrypt.items()}
    start_number = message.text.upper()

    try:
        start_number = ''.join(reversed(start_number))

        first_result = 0
        for i in range(len(start_number)):
            if start_number[i] in incrypt:
                first_result += incrypt[start_number[i]] * int(first_Encrypt) ** i
            else:
                raise ValueError

        duplicate = first_result
        result = ''
        while duplicate > 0:
            small_result = duplicate % second_Encrypt
            result += reverse_incrypt[small_result]
            duplicate //= second_Encrypt

        result = ''.join(reversed(result))
        bot.send_message(message.chat.id, f'Результат кодировки: {result}')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка: Пожалуйста, введите корректное число для кодировки.')

    show_encrypt_menu(message)


bot.polling(none_stop=True)
