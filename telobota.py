import random
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.utils import executor

# Настройка логирования для устранения ошибок
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token='6145805586:AAHXv7d5UvHOLe5qEx-K5qbUuM3SgqB02lU')
dp = Dispatcher(bot)

# Задаем диапазон, в котором будет загадываться число
minimum = 1
maximum = 10


# Функция для рандомного выбора числа
def generate_number():
    return random.randint(minimum, maximum)


# Глобальные переменные для хранения загаданного числа и количества попыток
number_to_guess = None
number_of_attempts = 0

# Клавиатура для выбора режима игры
game_mode_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
game_mode_keyboard.add(types.KeyboardButton("Я загадываю"), types.KeyboardButton("Бот загадывает"))


# Хэндлер для команды /start
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    global number_to_guess, number_of_attempts

    await message.answer("Привет! Я бот, который играет в игру 'Угадай число'. Выберите, кто будет загадывать число:",
                         reply_markup=game_mode_keyboard)


# Хэндлер для выбора режима игры
@dp.message_handler(Text(equals="Бот загадывает"))
async def bot_guesses_number(message: types.Message):
    global number_to_guess, number_of_attempts
    number_to_guess = generate_number()  # Загадываем число
    number_of_attempts = 0  # Задаем количество попыток на 0
    await message.answer("Я загадал число в диапазоне от {} до {}. Попробуйте отгадать его.".format(minimum, maximum))


# Хэндлер для принятия сообщений с числом
@dp.message_handler(lambda message: number_to_guess is not None)
async def guess_number(message: types.Message):
    global number_to_guess, number_of_attempts

    try:
        guess = int(message.text)
        number_of_attempts += 1  # Увеличиваем количество попыток на 1

        # Если пользователь отгадал число
        if guess == number_to_guess:
            await message.answer(
                "Ура, вы отгадали число за {} попыток! Наберите /start, чтобы начать новую игру.".format(
                    number_of_attempts))
            number_to_guess = None  # Сбрасываем загаданное число
            number_of_attempts = 0  # Задаем количество попыток на 0
        elif guess < number_to_guess:
            await message.answer("Загаданное число больше.")
        elif guess > number_to_guess:
            await message.answer("Загаданное число меньше.")
    except ValueError:
        await message.answer("Вы ввели не целое число")


# # Хэндлер для выбора режима игры
# @dp.message_handler(Text(equals="Я загадываю"))
# async def user_guessed_number(message: types.Message):
#     global number_to_guess, number_of_attempts
#     number_to_guess = None
#     number_of_attempts = 0  # Задаем количество попыток на 0
#     await message.answer("Введите число, которое я должен отгадать:")
#
#
# # Хэндлер для принятия загаданного числа пользователем
# @dp.message_handler(lambda message: number_to_guess is None)
# async def set_number_to_guess(message: types.Message):
#     global number_to_guess
#     try:
#         number_to_guess = int(message.text)
#         await message.answer("Загаданное число принято!")
#
#
#     except ValueError:
#         await message.answer("Вы ввели не целое число, попробуйте еще раз")


def main():
    executor.start_polling(dp, skip_updates=True)