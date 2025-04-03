from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()

class Data(StatesGroup):
    first_encrypt = State()
    second_encrypt = State()
    number = State()

async def encrypt(first_Encrypt, second_Encrypt, Number):
    incrypt = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
               'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    
    reverse_incrypt = {v: k for k, v in incrypt.items()}
    start_number = str(Number).upper()

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
    return result



@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer('Из какой кодировки переводим число?',
                         reply_markup=kb.main)
    await state.set_state(Data.first_encrypt)

@router.message(Data.first_encrypt)
async def get_first_encrypt(message: Message, state: FSMContext):
    await state.update_data(first_encrypt=message.text)
    data = await state.get_data()

    await state.set_state(Data.second_encrypt)

    await message.answer('В какую кодировку переводим?',
                         reply_markup=kb.main)

@router.message(Data.second_encrypt)
async def get_second_encrypt(message: Message, state: FSMContext):
    await state.update_data(second_encrypt=message.text)
    data = await state.get_data()

    await state.set_state(Data.number)

    await message.answer('Введите число для перевода',
                         reply_markup=kb.main)

@router.message(Data.number)
async def get_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)

    data = await state.get_data()

    result = await encrypt(int(data.get('first_encrypt')), int(data.get('second_encrypt')), data.get('number', ))

    await message.reply(f'Результат: {result}\nПовторим? /start')

@router.message(Command('help'))
async def help_text(message: Message):
    await message.answer('Помощь')
