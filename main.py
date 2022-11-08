import handlers
from create_bot import bot, dp
from aiogram import executor

async def onStart(_):
    print('Бот запущен и готов к работе')

handlers.registred_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=onStart)