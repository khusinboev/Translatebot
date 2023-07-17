from Handlers.AdminHandler import *
from Handlers.StartHandler import *
from Handlers.TranslateHandler import *
from aiogram import executor, types
from Configs import dp


if __name__ == '__main__':
    executor.start_polling(dp)
