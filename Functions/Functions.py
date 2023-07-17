from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from deep_translator import GoogleTranslator
from gtts import gTTS
from Configs import cur, dp, conn, langL1, langL2, langCode


async def UpgradeLang(callData, user_id):
    leftL = []
    for i in langL1:
        leftL.append(i)
    
    rightL = []
    for i in langL2:
        rightL.append(i)

    code = []
    for i in langCode:
        code.append(i)

    if callData == 'TTS':
        cur.execute(f"""SELECT tts FROM users WHERE user_id='{user_id}'""")
        boolen1 = cur.fetchone()[0]
        if boolen1 == True:
            cur.execute(f"update users set tts=false where user_id='{user_id}'")
            conn.commit()
        else:
            cur.execute(f"update users set tts=true where user_id='{user_id}'")
            conn.commit()

    elif callData in leftL:
        cur.execute(f"""SELECT lang_in FROM chooseLang WHERE user_id='{user_id}'""")
        langIn = cur.fetchone()
        if langIn == None:
            cur.execute(
                f"""INSERT INTO chooseLang (user_id, lang_in) VALUES ('{user_id}', '{callData}')""")
            conn.commit()
        else:
            cur.execute(f"update chooseLang set lang_in='{callData}' where user_id='{user_id}'")
            conn.commit()

    elif callData in rightL:
        cur.execute(f"""SELECT lang_out FROM chooseLang WHERE user_id='{user_id}'""")
        langIn = cur.fetchone()
        if langIn == None:
            cur.execute(
                f"""INSERT INTO chooseLang (user_id, lang_out) VALUES ('{user_id}', '{callData}')""")
            conn.commit()
        else:
            cur.execute(f"update chooseLang set lang_out='{callData}' where user_id='{user_id}'")
            conn.commit()

    else:
        pass


class functions:
    @staticmethod
    async def check_on_start(user_id):
        if user_id == 2129012886:
            return True
        else:
            cur.execute("SELECT id FROM channels")
            rows = cur.fetchall()
            error_code = 0
            for row in rows:
                r = await dp.bot.get_chat_member(chat_id=row[0], user_id=user_id)
                if r.status in ['left']:
                    error_code = 1
                else:
                    pass
            if error_code in [0, '']:
                return True
            else:
                return False


async def TranslateText(text, user_id):
    cur.execute(f"Select lang_in From chooseLang Where user_id='{user_id}'")
    langIn = cur.fetchone()[0]
    leftL = langCode[langL1.index(langIn)]

    cur.execute(f"Select lang_out From chooseLang Where user_id='{user_id}'")
    langOut = cur.fetchone()[0]
    rightL = langCode[langL2.index(langOut)]

    translator = GoogleTranslator(source=leftL, target=rightL)
    message = translator.translate(text)

    return message