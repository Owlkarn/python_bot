from aiogram import types, Dispatcher

import commands


def registred_handlers(dp: Dispatcher):
    dp.register_message_handler(commands.start, commands=['start'])
    dp.register_message_handler(commands.help, commands=['help'])
    dp.register_message_handler(commands.roll, commands=['roll'])
    dp.register_message_handler(commands.mode, commands=['mode'])
    dp.register_message_handler(commands.count, commands=['count'])
    dp.register_message_handler(commands.take, commands=['take'])
    dp.register_message_handler(commands.anything)