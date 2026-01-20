import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from gigachat import GigaChat
import os
from dotenv import load_dotenv

# Загружаем переменные
load_dotenv()

# Токены
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GIGACHAT_CREDENTIAL = os.getenv("GIGACHAT_CREDENTIAL")

# Инициализация
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Клиент GigaChat
giga = GigaChat(
    credentials=GIGACHAT_CREDENTIAL,
    scope="GIGACHAT_API_PERS",
    verify_ssl_certs=False
)

# Шаблоны (позже вы их замените)
FAQ = {
    "кредит": "Кредиты от 9,5% годовых. Сумма до 5 млн ₽. Подробнее: https://bank.ru/credits",
    "вклад": "Вклады от 10% годовых. Срок от 3 месяцев. Капитализация — ежемесячно.",
    "карта": "Дебетовая карта бесплатно. Кэшбэк до 10%. Доставка за 1 день.",
    "ипотека": "Ипотека от 6,5%. Первый взнос от 10%. Рассмотрение за 2 дня."
}

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Здравствуйте! Я — ваш банковский помощник.\n"
        "Задайте вопрос о кредите, вкладе, карте или ипотеке."
    )

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text.lower()

    # Проверяем шаблоны
    for key, answer in FAQ.items():
        if key in user_text:
            await message.answer(answer)
            return

    # Если нет — спрашиваем GigaChat
    try:
        response = giga.chat(f"Ты — консультант банка. Ответь кратко и вежливо. Вопрос: {user_text}")
        ai_text = response.choices[0].message.content
        await message.answer(ai_text)
    except Exception as e:
        await message.answer("Извините, временные неполадки. Попробуйте позже.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())