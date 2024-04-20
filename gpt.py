import asyncio
import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config

# Установка токена API ChatGPT
openai.api_key = config.gpt_key

# Инициализация бота и диспетчера
bot = Bot(token=config.token)
dp = Dispatcher(bot)


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Этот бот работает с ChatGPT. Отправьте мне ваш вопрос, и я постараюсь на него ответить!")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def generate_response(message: types.Message):
    try:
        # Генерация ответа от ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "User: " + message.text}
            ]
        )
        await message.answer(response.choices[0].message['content'])
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
