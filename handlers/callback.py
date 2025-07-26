from pickletools import bytes_types
from tkinter import Image

import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

total_cards = 5
user_progress = {}
def keyboard_for_card(card_number:int):
    if card_number < total_cards:
        buttons = [InlineKeyboardButton(text="▶️ Далее>", callback_data=f"card_{card_number+1}")]
    else:
        buttons = [InlineKeyboardButton(text="✅ Я запомнил, давай дальше", callback_data="remembered")]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
def get_card_content(card_number:int):
    photos ={
        1 : "media/photo/1.jpg",
        2 : "media/photo/2.jpg",
        3 : "media/photo/3.jpg",
        4 : "media/photo/4.jpg",
        5 : "media/photo/5.jpg",
    }

    captions ={
        1: """🌓 <b>Я — Геката, Триединая богиня.</b>
        Я — юная дева, зрелая женщина и старая ведьма
        Символизирую <b>три стадии жизни и три фазы луны</b>
        ➤ Растущая Луна — это начало твоего пути.
        ➤ Полнолуние — пик твоей силы.
        ➤ Старая Луна — тайна и мудрость, что приходит с опытом.
        Я — хранительница переходов и тайн между мирами.
             """,
        2: """🗝 <b>Меня почитали на перекрёстках и границах.</b>
        Я охраняю пороги между мирами — земным и потусторонним.
        Мои последователи приносили мне жертвы на перекрёстках дорог и возле кладбищ.
        Мои символы — ключи, факелы и собаки — всегда со мной.
        Я — страж тьмы и света, и мой свет ведёт в неизвестность.
                """,
        3: """<b>Смотри на мои символы — я говорю через них.</b>
        Мои три собаки — верные стражи, что сопровождают меня.
        Факелы освещают путь даже в самой густой тьме.
        Ключи открывают двери, что скрыты от посторонних глаз.
        Я — хранительница магии, знаний и древних секретов.
        """,
        4:  """<b>Я живу в глубинах твоего подсознания.</b>
Я — твой внутренний свет, что освещает тёмные уголки души.
Я помогаю пройти через страх, кризисы и перемены.
Слушай меня — и ты найдёшь силу принять тени и обрести мудрость.
Я — твой проводник в миры неизведанного внутри тебя.""",

    5:  """<b>Вот несколько моих тайн и историй.</b>
        1. Я — древняя богиня, чьё имя звучит сквозь века.
        2. Моё почитание живо до сих пор в магии и культуре.
        3. Меня зовут в ночи, когда нужен совет и защита.
        4. Я символизирую перемены и вечный цикл жизни.
        5. Мои тайны открываются тем, кто готов идти путём тени.
        Следуй за мной — и откроешь неизведанное."""
    }

    return photos[card_number], captions[card_number]

questions = [
    {
        "question": "Сколько ликов у Гекаты?",
        "options": ["Один", "Три", "Семь"],
        "correct": 1
    },
    {
        "question": "Что символизируют три фазы Луны у Гекаты?",
        "options": ["Жизненные этапы", "Стихии природы", "Времена года"],
        "correct": 0
    },
    {
        "question": "Где Гекате приносили дары?",
        "options": ["В храмах Афины", "На перекрёстках", "В морских пещерах"],
        "correct": 1
    },
    {
        "question": "Какие предметы Геката держит в руках?",
        "options": ["Косу и щит", "Факел, нож и ключ", "Жезл и кубок"],
        "correct": 1
    },
    {
        "question": "Какую роль Геката играет в психике человека?",
        "options": [
            "Прохождение через тьму бессознательного",
            "Символизирует успех и карьеру",
            "Защищает от болезней и голода"
        ],
        "correct": 0
    }
]

async def send_question(message, user_id):
    question_index = user_progress[user_id]["current_question"]
    question_data = questions[question_index]
    user_progress[user_id]["attempts"] = 2

    buttons = [
        [InlineKeyboardButton(text=opt, callback_data=f"answer_{i}")] for i, opt in enumerate(question_data['options'])
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(f"<b>{question_data['question']}</b>", reply_markup=markup, parse_mode="HTML")


@router.callback_query(F.data == "start")
async def next_handler(callback: CallbackQuery):
    await callback.message.answer("""
    <b>Ты ступил на путь Тени.</b>
     Чтобы обрести силу — нужно знать, кого ты зовёшь.
    Я — Геката. И у меня три лика.
    Посмотри на образы. Прочти, запомни. Потом — докажи, что внимал.
""", parse_mode="html")
    await callback.answer()
    await asyncio.sleep(2)

    card_number = 1
    photo_path, caption = get_card_content(card_number)
    photo = FSInputFile(photo_path)
    keyboard = keyboard_for_card(card_number)
    await callback.message.answer_photo(photo, caption=caption, parse_mode="html", reply_markup=keyboard)

@router.callback_query(F.data.startswith("card_"))
async def show_card(callback: CallbackQuery):
    card_number = int(callback.data.split("_")[1])
    photo_path, caption = get_card_content(card_number)
    photo = FSInputFile(photo_path)
    await callback.message.answer_photo(photo, caption=caption, parse_mode="HTML", reply_markup=keyboard_for_card(card_number))

@router.callback_query(F.data == "remembered")
async def remembered_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_progress[user_id] = {
        "current_question": 0,
        "correct_answers": 0,
        "attempts": 2
    }
    await callback.message.answer("""Отлично! Тогда продолжаем путь…
                                  И проверим твои знания""")
    await callback.answer()
    await asyncio.sleep(2)
    await send_question(callback.message, user_id)


@router.callback_query(F.data.startswith("answer_"))
async def handle_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    selected = int(callback.data.split("_")[1])
    progress = user_progress[user_id]

    question_index = progress["current_question"]
    correct = questions[question_index]["correct"]

    if selected == correct:
        progress["correct_answers"] += 1
        await callback.message.answer("✅ Верно!")
        progress["current_question"] += 1
        await callback.answer()
        await asyncio.sleep(1)
        if progress["current_question"] < len(questions):
            await send_question(callback.message, user_id)
        else:
            await finish_quiz(callback.message, user_id)
    else:
        progress["attempts"] -= 1
        if progress["attempts"] > 0:
            await callback.message.answer("❌ Неверно. Попробуй ещё раз. Осталась 1 попытка.")
            await callback.answer()
        else:
            await callback.message.answer(
                f"❌ Неверно. Правильный ответ: <b>{questions[question_index]['options'][correct]}</b>",
                parse_mode="HTML"
            )
            progress["current_question"] += 1
            await callback.answer()
            await asyncio.sleep(1)
            if progress["current_question"] < len(questions):
                await send_question(callback.message, user_id)
            else:
                await finish_quiz(callback.message, user_id)


async def finish_quiz(message, user_id):
    score = user_progress[user_id]["correct_answers"]
    total = len(questions)
    await message.answer(
    f"✨ Ты прошёл тест! Результат: <b>{score}/{total}</b>\n"
    "Ты прошёл испытание.\n"
    "Геката довольна.\n"
    "Она дарит тебе свой символ — знак силы, защиты и мудрости.\n"
    "🔮 <b>Прими дар — и иди дальше по пути Тени…</b>\n\n"
    "Спроси его у официанта и покажи результаты",
    parse_mode="HTML"
)
    del user_progress[user_id]
    await asyncio.sleep(1)
