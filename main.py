import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers import start, callback
from config import Config, load_config

config: Config = load_config()
#BOT_TOKEN: str = config.tg_bot.token



bot = Bot(token="7852599299:AAFZVgxzJjGn7k_luA3apQdc_yRa_7bn0kQ")
dp = Dispatcher()


dp.include_router(start.router)
dp.include_router(callback.router)




if __name__ == "__main__":
    dp.run_polling(bot)