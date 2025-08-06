from aiogram import Router, F
from aiogram.types import FSInputFile, Message
from aiogram.filters import CommandStart
from keyboards.main import get_start_keyboard
router = Router()

@router.message(CommandStart())
async def start(message: Message):
    photo = FSInputFile('media/photo/hekate_start_photo.jpg')
    caption = ("<b>Добро пожаловать, странник...</b>\n\n"
    "💫 Я — <b>Геката</b>. Приветствую тебя у моего алтаря.\n\n"
    "⚫ Здесь начинается путь не для всех.\n"
    "Это место — мир теней и тайн.\n"
    "Ты узнаешь то, чего не знал. Или вспомнишь то, что давно забыл.\n\n"
    "🔥 За твою смелость я дарую тебе <i>огонь познания</i> — он осветит твой путь\n"
    "и исполнит <b>одно желание</b>.\n\n"
    "Если решишь идти дальше —\n"
    "я открою тебе доступ к своей силе.\n\n"
    "<b>Готов ступить на тропу Магии?</b>")

    # Next Button

    await message.answer_photo(photo, caption=caption, parse_mode='HTML', reply_markup=get_start_keyboard())