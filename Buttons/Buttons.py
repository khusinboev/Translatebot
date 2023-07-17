from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from Configs import cur, dp, langL1, langL2, langCode


async def LangInline(user_id):
    cur.execute(f"SELECT lang_in from chooseLang where user_id='{user_id}'")
    check1 = cur.fetchone()
    cur.execute(f"SELECT lang_out from chooseLang where user_id='{user_id}'")
    check2 = cur.fetchone()
    if check1==None and check2==None:
        lang_btn = InlineKeyboardMarkup(row_width=2)
        for leftL, rightL, code in zip(langL1, langL2, langCode):
            lang_btn.add(InlineKeyboardButton(leftL, callback_data=leftL))
            lang_btn.insert(InlineKeyboardButton(rightL, callback_data=rightL))
        lang_btn.add(InlineKeyboardButton("☑TTS", callback_data='TTS'))

        return lang_btn
    else:

        lang_btn = InlineKeyboardMarkup(row_width=2)
        for leftL, rightL, code in zip(langL1, langL2, langCode):
            if check1[0] == leftL:
                lang_btn.add(InlineKeyboardButton("✅" + leftL, callback_data=leftL))
            else:
                lang_btn.add(InlineKeyboardButton(leftL, callback_data=leftL))
            if check2[0] == rightL:
                lang_btn.insert(InlineKeyboardButton("✅" + rightL, callback_data=rightL))
            else:
                lang_btn.insert(InlineKeyboardButton(rightL, callback_data=rightL))

        cur.execute(f"""SELECT tts FROM users WHERE user_id='{user_id}'""")
        boolen = cur.fetchone()[0]
        if boolen == True:
            lang_btn.add(InlineKeyboardButton("✅TTS", callback_data='TTS'))
        else:
            lang_btn.add(InlineKeyboardButton("☑TTS", callback_data='TTS'))

        return lang_btn


async def CheckJoinInline():
    cur.execute("SELECT id FROM channels")
    rows = cur.fetchall()
    join_inline = InlineKeyboardMarkup(row_width=1)
    title = 1
    for row in rows:
        all_details = await dp.bot.get_chat(chat_id=row[0])
        url = all_details['invite_link']
        join_inline.insert(InlineKeyboardButton(f"{title} - kanal", url=url))
        title += 1
    join_inline.add(InlineKeyboardButton("🔁 Tekshirish", callback_data='check'))

    return join_inline


adminBtn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
adminBtn.add("📈 Statistika", "📢️Kanallar", "✍Xabar yuborish")

channelsBtn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
channelsBtn.add("➕️Kanal qo'shish", "❌️Kanalni olib tashlash", "📋️Kanallar ro'yxati", "🔙Orqaga qaytish")

sendMsg = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
sendMsg.add("📬Forward message", "📃Simple message", "🔙Orqaga qaytish")

backBtn = ReplyKeyboardMarkup(resize_keyboard=True)
backBtn.add("⬅Orqaga qaytish")