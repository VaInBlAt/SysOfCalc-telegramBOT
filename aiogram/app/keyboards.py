from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='2'),
    KeyboardButton(text='8')],
    [KeyboardButton(text='10'),
    KeyboardButton(text='16')]],
    
    resize_keyboard=True,
    input_field_placeholder='Выберите СС')

 