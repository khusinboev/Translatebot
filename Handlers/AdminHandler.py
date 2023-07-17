import asyncio

import pytz
import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext

from Buttons.Buttons import adminBtn, channelsBtn, backBtn, sendMsg
from Configs import dp, cur, Admin
from Functions.adminFunction import panel_func, forward_send_msg, send_message_chats
from States.States import Form


@dp.message_handler(state='*', text="🔙Orqaga qaytish", user_id=Admin)
async def Statistic(message: types.Message, state: FSMContext):
    await message.answer("Bosh bo'lim", reply_markup=adminBtn)
    try:
        state.finish()
    except:
        pass


@dp.message_handler(commands='admin', user_id=Admin)
async def admin(message: types.Message):
    await message.answer("Assalomu alaykum admin", reply_markup=adminBtn)


@dp.message_handler(text=["📈 Statistika", "/static"], user_id=Admin)
async def Statistic(message: types.Message):
    today = datetime.datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%d-%m-%Y')
    cur.execute(f"Select COUNT(*) from users where active_date='{today}'")
    activeToday = cur.fetchone()[0]
    cur.execute(f"Select COUNT(*) from users where active_date='{today}'")
    cur.execute("SELECT COUNT(*) FROM users")
    followersall = cur.fetchone()[0]
    await message.answer(f"Bugun botdan foydalanganlar - {activeToday}\n\nHamma azolar soni - {followersall}")

#####################################################################################


@dp.message_handler(text="📢️Kanallar", user_id=Admin)
async def Statistic(message: types.Message):
    await message.answer("kanallar bo'limi", reply_markup=channelsBtn)


@dp.message_handler(text="➕️Kanal qo'shish", user_id=Admin)
async def addChannel(message: types.Message):
    await message.answer("Qo'shmoqchi bo'lgan kanalingiz userini yuboring\n\n"
                         "Faqat bu tartibda yuborish kerak: @coder_admin", reply_markup=backBtn)
    await Form.channelAdd.set()


@dp.message_handler(state=Form.channelAdd, user_id=Admin)
async def channelAdd(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == "⬅Orqaga qaytish":
        await message.answer("orqaga qaytildi", reply_markup=channelsBtn)
    else:
        channel_id = [message.text.upper()]
        cur.execute(f"SELECT id FROM channels WHERE id = '{message.text.upper()}'")
        data = cur.fetchone()
        if data is None:
            if message.text[0] == '@':
                await panel_func.channel_add(channel_id)
                try:
                    state.finish()
                except:
                    pass
                await message.reply("Kanal qo'shildi🎉🎉", reply_markup=channelsBtn)
            else:
                await message.reply("Kanal useri xato kiritildi\nIltimos userni @coder_admin ko'rinishida kiriting",
                                    reply_markup=channelsBtn)
        else:
            await message.reply("Bu kanal avvaldan bor", reply_markup=channelsBtn)
    try:
        state.finish()
    except:
        pass


@dp.message_handler(text="❌️Kanalni olib tashlash", user_id=Admin)
async def deleteChannel(message: types.Message):
    await message.answer("O'chirmoqchi bo'lgan kanalingiz userini yuboring\n\n"
                         "Faqat bu tartibda yuborish kerak: @coder_admin", reply_markup=backBtn)
    await Form.channelDelete.set()


@dp.message_handler(state=Form.channelDelete, content_types="text", user_id=Admin)
async def channelAdd(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == "⬅Orqaga qaytish":
        await message.answer("orqaga qaytildi", reply_markup=channelsBtn)
    else:
        channel_id = message.text.upper()
        cur.execute(f"""SELECT id FROM channels WHERE id = '{channel_id}'""")
        data = cur.fetchone()
        if data is None:
            await message.reply("Bunday kanal yo'q", reply_markup=channelsBtn)
        else:
            if message.text[0] == '@':
                await panel_func.channel_delete(channel_id)
                try:
                    state.finish()
                except:
                    pass
                await message.reply("Kanal muvaffaqiyatli o'chirildi", reply_markup=channelsBtn)
            else:
                await message.reply("Kanal useri xato kiritildi\nIltimos userni @coder_admin ko'rinishida kiriting",
                                    reply_markup=channelsBtn)
    try:
        state.finish()
    except:
        pass


@dp.message_handler(text="📋️Kanallar ro'yxati", user_id=Admin)
async def channelList(message: types.Message):
    if len(await panel_func.channel_list()) > 3:
        await message.reply(await panel_func.channel_list())
    else:
        await message.reply("Hozircha kanallar yo'q")

####################################################################


@dp.message_handler(text="✍Xabar yuborish", user_id=Admin)
async def sentMsg(message: types.Message):
    await message.answer("Messaging section", reply_markup=sendMsg)


@dp.message_handler(text="📬Forward message", user_id=Admin)
async def SendForward(message: types.Message):
    await message.answer("Forward yuboriladigan xabarni yuboring", reply_markup=backBtn)
    await Form.forward_msg.set()


@dp.message_handler(state=Form.forward_msg, user_id=Admin)
async def sendForward(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == "⬅Orqaga qaytish":
        await message.answer("orqaga qaytildi", reply_markup=sendMsg)
        try:
            state.finish()
        except:
            pass
    else:
        cur.execute(f"SELECT user_id FROM users ")
        rows = cur.fetchall()
        nomr = 0
        await message.answer("xabar yuborish boshlandi", reply_markup=adminBtn)
        for row in rows:
            id = row[0]
            raqami = await forward_send_msg(from_chat_id=message.chat.id, message_id=message.message_id, chat_id=id)
            if raqami == True:
                nomr += 1
            await asyncio.sleep(0.07)

        await message.answer(f"Xabar yuborish yakunlandi. Bu xabar {nomr} ta odamga yuborildi")
        try:
            state.finish()
        except:
            pass


@dp.message_handler(text= "📃Simple message", user_id=Admin)
async def SendSimple(message: types.Message):
    await message.answer("Yuborilishi kerak bo'lgan xabarni yuboring", reply_markup=backBtn)
    await Form.send_msg.set()


@dp.message_handler(state=Form.send_msg, user_id=Admin)
async def sendSimple(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == "⬅Orqaga qaytish":
        await message.answer("orqaga qaytildi", reply_markup=sendMsg)
        try:
            state.finish()
        except:
            pass
    else:
        cur.execute(f"SELECT user_id FROM users ")
        rows = cur.fetchall()
        soni = 0
        await message.answer("xabar yuborish boshlandi", reply_markup=adminBtn)
        for row in rows:
            id = row[0]
            raqami = await send_message_chats(from_chat_id=message.chat.id, message_id=message.message_id, chat_id=id)
            soni += raqami
            await asyncio.sleep(0.07)

        await message.answer(f"Xabar yuborish yakunlandi. Bu xabar {soni} ta odamga yuborildi")

        try:
            state.finish()
        except:
            pass
