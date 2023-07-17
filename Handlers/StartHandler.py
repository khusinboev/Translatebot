import datetime
import pytz
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from Configs import *
from Buttons.Buttons import *


@dp.message_handler(state='*', commands='start')
async def send_welcome(message: types.Message):
    try:
        state.finish()
    except:
        pass
    userId = message.from_user.id
    cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id VARCHAR(15) NOT NULL, 
                    date VARCHAR(20), active_date VARCHAR(20), lang varchar(10), tts BOOL)""")
    conn.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS channels(id VARCHAR)")
    conn.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS chooseLang(user_id VARCHAR(15) NOT NULL, 
                    lang_in VARCHAR(15), lang_out VARCHAR(15))""")
    conn.commit()
    cur.execute(f'''SELECT * from users where user_id='{userId}' ''')
    check = cur.fetchone()
    sana = datetime.datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%d-%m-%Y')

    if check == None:
        cur.execute(
            f"""INSERT INTO users (user_id, date) VALUES ('{userId}', '{sana}')""")
        cur.execute(f"update users set tts=true where user_id='{userId}'")
        conn.commit()
        cur.execute(f"update users set active_date='{sana}' where user_id='{userId}'")
        conn.commit()
 
    main_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    main_btn.add("🇺🇿Uzbek", "🇬🇧English", "🇷🇺Русский")
    await message.reply("Tilni tanlang 👇\nChoose the language 👇\nВыберите язык 👇", reply_markup=main_btn)


@dp.message_handler(text=["🇺🇿Uzbek", "🇬🇧English", "🇷🇺Русский"])
async def check(message: types.Message):
    try:
        userId = message.from_user.id
        lang = {"🇺🇿Uzbek":"uz", "🇬🇧English":"en", "🇷🇺Русский":"ru"}
        cur.execute(f"update users set lang='{lang[message.text]}' where user_id='{userId}'")
        conn.commit()
        
        textL = {"🇺🇿Uzbek":textUz, "🇬🇧English":textEn, "🇷🇺Русский":textRu}
        text2 = {"🇺🇿Uzbek":"Botdan foydalanish bo'yicha qo'llanma", "🇬🇧English":"A guide to using the bot", "🇷🇺Русский":'Руководство по использованию бота'}
        text = str(textL[message.text])
        await message.answer_video(video="BAACAgIAAxkBAAEpBTRkfcSHpKNbKHU9qCwgEXQS65i36AACJDEAAjYx0EuI681ovTz5DC8E",
                                caption=str(text2[message.text]), reply_markup=ReplyKeyboardRemove())
        await message.answer(text=text, reply_markup=await LangInline(userId))
    except:
        await message.answer('/start')
