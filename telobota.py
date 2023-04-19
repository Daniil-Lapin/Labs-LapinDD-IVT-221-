import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
import asyncio

# Настройка логирования для устранения ошибок
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token='6145805586:AAHXv7d5UvHOLe5qEx-K5qbUuM3SgqB02lU')
dp = Dispatcher(bot)

# Задаем диапазон, в котором будет загадываться число
minimum = 1
maximum = 10

numbers = {}

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




@dp.message_handler(Text(equals="Я загадываю"))
async def start(message: types.Message):
    await message.answer("Загадайте число и скажите в каком диапозоне мне искать(Напишите: 100 (если от 1 до 100))")

@dp.message_handler(Text(equals=["да", "нет"]))
async def check_answer(message: types.Message):
    chat_id = message.chat.id
    if message.text.lower() == "да":
        await bot.send_message(chat_id, "Ура, я сегодня в ударе!!!")
        del numbers[chat_id]
    else:
        await bot.send_message(chat_id, "Хорошо, продолжим")
        await guess_number(message)

@dp.message_handler()
async def guess_number(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in numbers:
        numbers[chat_id] = {}
        numbers[chat_id]['min'] = 1
        numbers[chat_id]['max'] = int(message.text)
        numbers[chat_id]['numbers'] = []
        numbers[chat_id]['tries'] = 0
    try2guess = random.randint(numbers[chat_id]['min'], numbers[chat_id]['max'])
    while try2guess in numbers[chat_id]['numbers']:
        try2guess = random.randint(numbers[chat_id]['min'], numbers[chat_id]['max'])
    numbers[chat_id]['numbers'].append(try2guess)
    numbers[chat_id]['tries'] += 1
    await message.answer(f"Ваше число: {try2guess}")
    await message.answer("Я угадал?")
    answer = await dp.register_message_handler(check_answer, message=message)
    if answer.text.lower() == "нет":
        if try2guess < numbers[chat_id]['max']:
            numbers[chat_id]['min'] = try2guess + 1
        else:
            numbers[chat_id]['max'] = try2guess - 1
        await guess_number(message)
    else:
        await message.answer(f"Я угадал ваше число за {numbers[chat_id]['tries']} попыток")
        del numbers[chat_id]
def main():
    executor.start_polling(dp, skip_updates=True)