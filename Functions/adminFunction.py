import asyncio
from aiogram import *
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, RetryAfter

from Configs import cur, dp, conn


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


class panel_func:
    @staticmethod
    async def channel_add(id):
        cur.execute(f'''INSERT INTO channels VALUES('{id[0]}')''')
        conn.commit()

    @staticmethod
    async def channel_delete(id):
        cur.execute(f'''DELETE FROM channels WHERE id = '{id}' ''')
        conn.commit()

    @staticmethod
    async def channel_list():
        cur.execute("SELECT id from channels")
        str = ''
        for row in cur.fetchall():
            id = row[0]
            try:
                all_details = await dp.bot.get_chat(chat_id=id)
                title = all_details["title"]
                channel_id = all_details["id"]
                info = all_details["description"]
                str += f"------------------------------------------------\nKanal useri: > {id}\nKamal nomi: > {title}\nKanal id si: > {channel_id}\nKanal haqida: > {info}\n"
            except:
                str += "Kanalni admin qiling"
        return str


async def forward_send_msg(chat_id: int, from_chat_id: int, message_id: int):
    try:
        await dp.bot.forward_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
        return True
    except exceptions.BotBlocked:
        return False
    except exceptions.ChatNotFound:
        return False
    except RetryAfter as Flood:
        await asyncio.sleep(Flood.timeout)
        is_sended = await dp.bot.forward_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
        if is_sended:
            return True
        else:
            return False

    except exceptions.UserDeactivated:
        return False

    except exceptions.MigrateToChat:
        try:
            await dp.bot.forward_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
            return True
        except:
            return False

    except exceptions.TelegramAPIError:
        try:
            await dp.bot.forward_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
            return True
        except:
            return False


async def send_message_chats(chat_id: int, from_chat_id: int, message_id: int) -> int:
    try:
        await dp.bot.copy_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
        return 1
    except:
        return 0
