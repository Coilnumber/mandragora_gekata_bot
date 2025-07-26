from aiogram import Router, F
from aiogram.types import FSInputFile, Message
from aiogram.filters import CommandStart
from keyboards.main import get_start_keyboard
router = Router()

@router.message(CommandStart())
async def start(message: Message):
    photo = FSInputFile('media/photo/hekate_start_photo.jpg')
    caption = """
        🔮 <b>Добро пожаловать, странник...</b>
        Ты подошёл к Алтарю Гекаты — богини перекрёстков, тени, магии и переходов.

        ⚫ Здесь начинается путь не для всех.
        Это место — мир теней, загадок и таинства.
        В нём ты узнаешь то, чего не знал о себе. Или вспомнишь то, что забыл.

        За твоё внимание и смелость я открою тебе малую тайну Мандрагоры — напиток или угощение, которое согреет тебя в этом мире.
        Но если ты решишь пойти дальше — я открою тебе доступ к своей силе.
        🕯️ <b>Готов ступить на тропу Магии?</b>
    """

    # Next Button

    await message.answer_photo(photo, caption=caption, parse_mode='HTML', reply_markup=get_start_keyboard())