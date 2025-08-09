from pickletools import bytes_types
from tkinter import Image

import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

router = Router()

total_cards = 7
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
        6:  "media/photo/6.jpg",
        7: "media/photo/7.jpg",
    }

    captions ={
        1: "🕯<b>Я зародилась во тьме доисторических времён.</b>\n\n"
           "🌒<b>Мой культ сохраняли на протяжении 3 тысячелетий.</b>\n\n"
        "Я пережила <b>древнюю Грецию</b>,античный Рим и <b>Византийскую империю.</b>\n"
        "Я пережила cредневековье и мне поклонялись в эпоху <b>Возрождения</b>\n\n"
        "⚖️<b>Я богиня Судьбы</b>.\n"
        "<b>Дева, Мать и Старуха</b>, в мою честь строили храмы и меня почитали с начала времен.\n"
        "С тех пор как магия пришла в этот мир.\n\n"
        "🌌<b>Я многоликая бесконечная женская сила.</b>\n\n"
        "<b>🗝 Ты нашёл меня</b>\n"
        "🔥 Сейчас ты у моего алтаря\n"
        "<b>💫 Открой своё сердце для магии</b>\n"
        ,
        2: "🔱 <b>Я — Богиня перекрёстков</b>, властительница судеб, открывающая любые двери и тайны.\n\n"
    
        "🌌 <b>Мне подвластны три мира:</b>\n"
        "— <i>Небо</i> — <i>Море</i> — <i>Земля</i>\n\n"
    
        "✨ <b>Я несу свет, красоту и силу.</b>\n"
        "Наполняю мир радостью, здоровьем и жизнью.\n\n"
    
        "🛡 <b>Я — защитница детей и слабых.</b>\n"
        "Гневная и Необоримая. Я укрываю от зла — и отвращаю его.\n\n"
    
        "⚖️ <b>Помни о балансе:</b>\n"
        "Что посеешь — то и пожнёшь.\n"
        "Сеешь смуту — получишь бурю.\n\n"
    
        "💡 <b>Используй мой свет с умом.</b>\n"
        "Пусть твоё желание несёт благо.\n\n"
    
        "🔮 <b>Ты можешь обращаться ко мне по-разному:</b>\n"
        "— Лучезарная, Светоносная\n"
        "— Тёмная Мать\n"
        "— Ключница\n"
        "— Королева Луны\n"
        "— Необоримая Спасительница",

        3:    "🏛 <b>Мне поклонялись в храмах и под звёздным небом</b>, на перекрёстках всех дорог.\n"
        "Люди ставили мои статуи, приносили дары и просили показать путь.\n\n"
        
        "🌍 <b>Мои алтари есть по всему миру.</b>\n"
        "Я стала частью разных культур и народов.\n\n"
    
        "📜 <b>Согласно древним мифам:</b>\n"
        "Я родилась во Фракии — Балканский полуостров.\n"
        "А мой самый известный храм находился в Лагине, на территории современной Турции.\n\n"
    
        "🔥 <b>Я — неотделимая часть Мира.</b>\n"
        "И живу в каждой душе, потому мои храмы стали появляться повсюду.\n"
        "Так я стала одной из важнейших богинь античного мира.\n\n"
    
        "🌕 <b>И ты всегда можешь найти меня, если пожелаешь.</b>\n"
        "Сейчас меня почитают в <i>Мандрагоре</i>, и мой алтарь открыт для тебя.",

        4:  "<b>Прикоснись ко мне — и я помогу тебе…</b>\n\n"
        "Мои атрибуты силы и власти:\n\n"
        "🔑 <b>Ключ</b> — открывает любые двери и тайны.\n"
        "🔥 <b>Факел</b> — освещает путь, дарует свет и знание.\n"
        "🗡 <b>Кинжал</b> — отсекает лишнее: прошлое от будущего, истину от лжи.\n"
        "⚖️ <b>Плеть</b> — обуздывает пороки, страсти и мимолётные желания.\n"
        "🧣 <b>Вуаль</b> — завеса между мирами, которую я могу приоткрыть для тебя.\n\n"
        "🌿 <b>Мандрагора — моя обитель…</b>\n\n"
        "Ты можешь взять с собой <b>мой амулет</b> или <b>талисман</b>\n"
        "с <i>древа познания Добра и Зла</i>.\n\n"
        "Он станет твоим проводником и защитой\n",

    5:  "<b>Я прихожу не одна…</b>\n\n"
        "Меня сопровождают верные создания Тьмы и Ночи —\n"
        "мои фамильяры, тотемные духи и помощники:\n\n"
        "🦉 <b>Совы и вороны</b> — летают между мирами, несут знание и мудрость.\n"
        "🐕 <b>Гончие псы</b> — мои стражи и защитники, истребляющие зло.\n"
        "🐍 <b>Змеи</b> — символ чистого знания, восходящего из самой Земли.\n"
        "🐸 <b>Лягушки, жабы и ящерицы</b> — архетип Женского Начала, пришедшего из глубин.\n"
        "🦅 <b>Грифоны и фениксы</b> — тотемы колдовства и трансформации души.\n\n"
        "🌑 Хочешь пробудить свою тотемную силу?\n"
        "Приходи на мои <b>мистерии Новолуния и Полнолуния</b>\n"
        "в <i>Мандрагоре</i>…",
    6: "Я всегда рядом — в твоей душе, в тени сознания.\n"
        "🗝 Я — проводник, отворяющий двери.\n\n"
        "🌘 Я скрыта во тьме, за завесой, между мирами.\n"
        "Как Луна, я прихожу ночью — через сны, знаки, мимолётные подсказки Вселенной.\n\n"
        "🐇 Я — кроличья нора, ведущая в страну чудес… и безумный страх перед неизвестным.\n"
        "☠️ Я — яд и исцеляющее лекарство.\n\n"
        "<b>Готов ли ты сделать шаг навстречу?</b>\n\n"
        "✨ Ибо я — в жажде перемен, новых путей и знаний.\n"
        "Я помогаю меняться, находить <i>мудрость</i> и <i>свой Путь</i>.\n\n"
        "🔮 Я говорю с тобой через моих верных проводников —\n"
        "<b>гадалок и оракулов</b>, что ответят на любые твои вопросы…",
    7:  "🕯️ <b>Даже сегодня, в новом времени — вы не забыли меня.</b>\n\n"
    "Ведь я — в каждой женщине и каждом мужчине, живу в твоей психике как <b>Тень</b>.\n"
    "Я — психопомп, проводник между мирами, освещающий твой путь.\n\n"
    "🌌 <b>Я — архетипическая сила внутри тебя, космос и голос души — неизведанные земли твоего сердца.</b>\n\n"
    "Я живу в древних шаманских обрядах, в волшебных книгах, в магии, колдовстве и ведьмовстве,\n"
    "в творчестве, искусстве и музыке.\n\n"
    "✨ Если ты читаешь это — я уже рядом.\n"
    "Прими меня — и ты станешь целостным.\n\n"
    "🚪 Мой путь начинается прямо здесь — и если ты хочешь пойти со мной,\n"
    "приходи на курс <b>«Древние Боги» в Калипсо</b>."
    }

    return photos[card_number], captions[card_number]

questions = [
    {
        "question": "Какие три женских лика я собой являю?",
        "options": ["Вера, Надежда, Любовь", "Дева, Мать, Старуха", "Дочь, Возлюбленная, Муза", "Феменистка, Богиня фитнеса, Инфоцыганка"],
        "correct": 1
    },
    {
        "question": "Какой принцип я несу в этом мире?",
        "options": ["Вселенная любит драму", "Карма и переселение душ ", "Баланс и равновесие", "Больше двух говорят вслух"],
        "correct": 2
    },
    {
        "question": "Где зародился мой культ?",
        "options": ["В Твиттере", "В Египте, среди песков и кошек","На улице Правды, дом 4", "Во Фракии, на Балканском полуострове"],
        "correct": 3
    },
    {
        "question": "Что является моими атрибутами и символами власти?",
        "options": ["Плеть и вуаль","Смузи и золотая кредитка", "Факел, нож и ключ", "Газнокосилка и тесла"],
        "correct": 2
    },
    {
        "question": "Кто является моими cпутниками Тьмы и Ночи?",
        "options": [
            "Крош, Бараш, Лосяш",
            "Морские свинки, павлины, пингвины",
            "Совы, вороны и змеи, гончие",
            "Дарт Вейдер и Хоакин Феникс"
        ],
        "correct": 2
    },
{
        "question": "Чем я помогаю человеку?",
        "options": [
            "Притянуть деньги и мужа",
            "Открыть чакры соседям",
            "Отстоять очередь в поликлиннике",
            "Меняться, находить правильный путь"
        ],
        "correct": 3
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
    await callback.message.answer("<b>Ты ступил на путь Тени.</b>\n\n"
    "Чтобы обрести силу — нужно знать, кого ты зовёшь.\n\n"
    "Я — <b>Геката</b>. И у меня <b>три лика</b>.\n\n"
    "<i>Посмотри на образы. Прочти, запомни. Потом — докажи, что внимал.</i>"
,
                                  parse_mode="html")
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
    await callback.message.answer(
        "<b>Отлично!</b> Тогда продолжаем путь…\n\n"
    "<i>И проверим твои знания</i>", parse_mode='HTML')
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
        await callback.message.answer("✔️ Верно! Ты внимал — и получил моё одобрение.")
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
            await callback.message.answer("❌ Нет. Сосредоточься и выбери мудро — осталась лишь одна попытка.")
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
    "Она дарит тебе свой свет, дабы осветить <b>твой путь.</b>\n"
    "🕯 <b>Прими дар — и используй его во благо</b>🙏\n\n"
    "Покажи результат бармену и он направит тебя",
    parse_mode="HTML"
)
    del user_progress[user_id]
    await asyncio.sleep(15)

    photo = FSInputFile("media/photo/fire.jpg")

    await message.answer_photo(photo = photo,
         caption= "🕯 <b>Ты получил мой дар...</b>\n\n"
            "✨ <i>Подумай о своём истинном желании.</i>\n"
            "Согрей свечу в ладонях — пусть она впитает твою энергию.\n"
            "Когда будешь готов — зажги её на алтаре Гекаты.\n\n"
            "🔥 <b>Смотри на пламя — это глаз Великой Богини.</b>\n"
            "Визуализируй результат своего желания.\n"
            "Почувствуй, как оно уже воплощается в реальности.\n"
            "<i>Пусть нет сомнений — воля твоя услышана.</i>\n\n"
            "🔮 <i>Если у тебя есть амулет — пронеси его через пламя,</i>\n"
            "<i>чтобы Геката наполнила его своей силой.</i>\n"
            "Он станет твоим проводником в мире Теней и Защиты.\n\n"
            "📜 Возьми пергамент — напиши на нём свои желания, цели, намерения.\n"
            "Будь честен с собой и с Богиней.\n"
            "Сложи его и опусти в <i>Сундук Гекаты</i>.\n"
            "На Великой Мистерии твои слова будут отданы Огню,\n"
            "и вместе с дымом достигнут Трёхликой.\n\n"
            "🌑 <i>Помни: Геката ведёт тех, кто готов идти во Тьму,\n"
            "чтобы там найти Свет.</i>"
        ,parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Геката, я завершил(а)', callback_data='hekata_return')]
        ],
        )
    )

@router.callback_query(F.data == "hekata_return")
async def second_part(callback: CallbackQuery):

     await callback.message.answer(text="<b>Поздравляю!</b>\n"
    "Ты прошёл большой путь\n"
    "И заручился моей поддержкой для своих свершений.\n\n"
    "<b>Мандрагора</b> — волшебное место, где я и другие Боги помогают людям.\n"
    "Здесь гадают, проводят лекции и беседы за чаем,\n"
    "смотрят кино и просто весело проводят время!\n\n"
    "Чтобы быть в курсе всех событий, подписывайся на наш канал:\n"
    "<a href='https://t.me/mandragoracafe'>t.me/mandragoracafe</a>\n\n"
    "И да прибудут с тобой Боги!",
                                   parse_mode="HTML")
