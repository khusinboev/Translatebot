from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
from gtts import gTTS

from Handlers.AdminHandler import *
from Buttons.Buttons import LangInline, CheckJoinInline
from Configs import dp, cur, conn, langL1, langL2, langCode, textEn, textRu, textUz
from Functions.Functions import UpgradeLang, functions, TranslateText


@dp.message_handler(commands='lang')
async def translate(message: types.Message):
    try:
        userId = message.from_user.id
        cur.execute(f"Select lang From users Where user_id='{userId}'")
        userLang = cur.fetchone()[0]

        textUz = "O'zingiz kerakli tillarni tanlang"
        textEn = "Choose the languages you want"
        textRu = "Выберите языки, которые вы хотите"

        textL = {"uz": textUz, "en": textEn, "ru": textRu}
        text = str(textL[userLang])
        await message.answer(text=text, reply_markup=await LangInline(userId))
    except:
        await message.answer('/start')


@dp.message_handler(content_types="text")
async def translate(message: types.Message):
    try:
        user_id = message.from_user.id
        name = message.from_user.first_name
        text = await TranslateText(message.text, user_id)
        if await functions.check_on_start(message.chat.id) or user_id in Admin:
            cur.execute(f"Select tts From users Where user_id='{user_id}'")
            userTts = cur.fetchone()[0]
            if userTts == True:
                cur.execute(f"Select lang_out From chooseLang Where user_id='{user_id}'")
                langOut = cur.fetchone()[0]
                leftL = langCode[langL2.index(langOut)]
                try:
                    tts = gTTS(text=text, lang=leftL)
                    tts.save(f'Audios/{name}-{user_id}.mp3')
                    await message.answer_audio(audio=open(f"Audios/{name}-{user_id}.mp3", 'rb'), caption=text)
                except ValueError:
                    await message.answer(text)
                except AssertionError:
                    await message.answer(message.text)
            else:
                await message.answer(text)
        else:
            await message.answer("Join the channels", reply_markup=await CheckJoinInline())

        sana = datetime.datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%d-%m-%Y')
        cur.execute(f'''SELECT active_date from users where user_id='{user_id}' ''')
        check = cur.fetchone()[0]
        if check != sana:
            cur.execute(
                f"update users set active_date='{sana}'"
                f" where user_id='{user_id}'")
            conn.commit()
    except(Exception):
        await message.answer('/start')
            


@dp.callback_query_handler()
async def choosL(call: CallbackQuery):
    try:
        user_id = call.from_user.id
        await UpgradeLang(call.data, user_id)

        cur.execute(f'''SELECT lang from users Where user_id='{user_id}' ''')
        lang = cur.fetchone()[0]
        answerL = {"uz":"✅Tanlandi", "en":"✅Selected", "ru":"✅Выбрано"}
        answerText = {"uz":textUz, "en":textEn, "ru":textRu}

        try:
            # await call.message.edit_text(text=str(answerText[lang]))
            await call.message.edit_reply_markup(await LangInline(user_id))
        except MessageNotModified:
            pass
        await call.answer(text=str(answerL[lang]))
    except:
        await call.message.answer('/start')
