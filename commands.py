import random

from aiogram import types

from create_bot import bot

candies = 150
max_candies_in_round = 28
coin = -1
players_candies = 0
comp_candies = 0
first_turn_fail = False


async def start(message: types.Message):
    global candies, max_candies_in_round, coin, players_candies, comp_candies, first_turn_fail
    candies = 150
    max_candies_in_round = 28
    coin = -1
    players_candies = 0
    comp_candies = 0
    first_turn_fail = False
    await bot.send_message(message.from_user.id,
                           f'Ну что, {message.from_user.first_name}, сыграем в конфеты? '
                           f'У меня на столе лежит {candies} конфет. '
                           f'За один ход ты можешь взять от 1 до {max_candies_in_round} конфет. '
                           f'Введи команду /roll для определения очередности хода. '
                           f'1 - ходишь первым ты, 0 - я.')


async def roll(message: types.Message):
    global coin, comp_candies, candies, max_candies_in_round, first_turn_fail
    coin = random.randint(0, 1)
    await bot.send_message(message.from_user.id,
                           f'И выпадает..... {coin}!!!')
    if coin == 0:
        await bot.send_message(message.from_user.id,
                               f'Не повезло, {message.from_user.first_name}, я хожу первым!')
        comp_candies = candies % (max_candies_in_round + 1)

        if comp_candies == 0:
            comp_candies = 1
            first_turn_fail = True

        candies -= comp_candies
        await bot.send_message(message.from_user.id,
                               f'Я взял {comp_candies} конфет! Осталось {candies}! '
                               f'Твоя очередь ходить! Возьми от 1 до 28 конфет.')
    else:
        await bot.send_message(message.from_user.id,
                               'Повезло! Ходи первым!')


async def anything(message: types.Message):
    global coin, candies, players_candies, first_turn_fail, comp_candies, max_candies_in_round
    if coin == -1:
        await bot.send_message(message.from_user.id,
                               'Не торопись! Сначала нужно определить очередность хода!')
    else:
        if candies > 0:
            players_candies = int(message.text)
            if players_candies < 1 or players_candies > 28:
                await bot.send_message(message.from_user.id,
                                       'В задании же сказано от 1 до 28 конфет! Вводи заново!')

            else:
                candies -= players_candies
                if candies <= 0:
                    await bot.send_message(message.from_user.id,
                                           'Поздравляю! Ты выиграл! Все конфеты твои!')

                await bot.send_message(message.from_user.id,
                                       f'Ты взял {players_candies} конфет. Осталось {candies} конфет! Моя очередь ходить!')

                if first_turn_fail:
                    comp_candies = candies % (max_candies_in_round + 1)
                    if comp_candies > candies:
                        comp_candies = candies
                        candies = 0
                        await bot.send_message(message.from_user.id,
                                               f'Я взял {comp_candies} конфет! Конфет не осталось! Я выиграл!')
                    elif comp_candies == 0 or comp_candies > 28:
                        comp_candies = 1
                        first_turn_fail = True
                    else:
                        first_turn_fail = False
                    candies -= comp_candies

                    await bot.send_message(message.from_user.id,
                                           f'Я взял {comp_candies} конфет! Осталось {candies}! Твоя очередь ходить!')

                elif (candies > (max_candies_in_round * 2)) or (candies == max_candies_in_round + 1):
                    comp_candies = max_candies_in_round + 1 - players_candies
                    candies -= comp_candies
                    await bot.send_message(message.from_user.id,
                                           f'Я взял {comp_candies} конфет! Осталось {candies}! Твоя очередь ходить!')

                elif (max_candies_in_round + 1) < candies < (max_candies_in_round * 2 + 1):
                    comp_candies = candies - max_candies_in_round - 1
                    candies -= comp_candies
                    await bot.send_message(message.from_user.id,
                                           f'Я взял {comp_candies} конфет! Осталось {candies}! Твоя очередь ходить!')

                else:
                    comp_candies = candies
                    candies = 0
                    await bot.send_message(message.from_user.id,
                                           f'Я взял {comp_candies} конфет! Конфет не осталось! Я выиграл!')
        else:
            await bot.send_message(message.from_user.id,
                                   'Игра окончена! Чтобы начать новую игру введи /start')

