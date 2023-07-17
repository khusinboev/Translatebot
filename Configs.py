from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import psycopg2

bot = Bot(token="5098772001:AAHum6l1NnQdnHPcXK0qeyTjgn6hEKMEggk")
dp = Dispatcher(bot, storage=MemoryStorage())

conn = psycopg2.connect(database="users", user='postgres', password='paro!123', host='127.0.0.1', port='5432')
cur = conn.cursor()

Admin = [5246872049, 1918760732]

langL1 = ["🇺🇿O`zbek", "🇹🇷Turk", "🇹🇯Tajik", "🇬🇧English", "🇯🇵Japan", "🇮🇹Italian", "🇷🇺Русский", "🇰🇷Korean", "🇸🇦Arabic",
            "🇨🇳Chinese", "🇫🇷French", "🇩🇪German", "🇮🇳Hindi", "🇦🇿Azerbaijan", "🇦🇫Afghan", "🇰🇿Kazakh", "🇹🇲Turkmen", "🇰🇬Kyrgyz"]

langL2 = ["🇺🇿 O`zbek", "🇹🇷 Turk", "🇹🇯 Tajik", "🇬🇧 English", "🇯🇵 Japan", "🇮🇹 Italian", "🇷🇺 Русский", "🇰🇷 Korean", "🇸🇦 Arabic",
            "🇨🇳 Chinese", "🇫🇷 French", "🇩🇪 German", "🇮🇳 Hindi", "🇦🇿 Azerbaijan", "🇦🇫 Afghan", "🇰🇿 Kazakh", "🇹🇲 Turkmen", "🇰🇬 Kyrgyz"]

langCode = ["uz", "tr", "tg", "en", "ja", "it", 'ru', 'korean', 'ar', 'zh-CN', 'fr', 'de', 'hi', 'az', 'af', 'kk', 'tk', 'ky']

textUz = """Assalomu alaykum😉.
Bot 1️⃣8️⃣ ta tilda tarjimonlik qila oladi♻️.
Bot faqat matnlar bilan ishlay oladi 📝.
Botda TTS funksiyasi ham bor lekin hamma tillarda emas🔊.

Tillar menusini chiqarish uchun pastdagi tugmani bosing yoki /lang kommandasidan foydalaning.✅"""
textEn = """Greetings.
The bot can translate 1️⃣8️⃣ languages♻️.
The bot can only work with texts 📝.
The bot also has a TTS function, but not in all languages🔊.

Click the button below or use the /lang command to bring up the language menu✅"""
textRu = """Привет.
Бот может переводить на 1️⃣8️⃣ языков♻️.
Бот умеет работать только с текстами 📝.
В боте также есть функция TTS, но не на всех языках🔊.

Нажмите кнопку ниже или используйте команду /lang, чтобы открыть языковое меню✅."""
