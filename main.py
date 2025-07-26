import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers import start, callback


bot = Bot(token='7983877425:AAEqs4Su7COXoSPTL-m0QOBtKZJ824-1kSQ')
dp = Dispatcher()


dp.include_router(start.router)
dp.include_router(callback.router)




if __name__ == "__main__":
    dp.run_polling(bot)