import random

from aiogram import types

from create_bot import bot

candies = 150
max_candies_in_round = 28
coin = -1
players_candies = 0
comp_candies = 0
game_mode = 1
first_turn_fail = False
select_game_mode = False
candies_count = False
candies_take = False


async def start(message: types.Message):
    global candies, max_candies_in_round, coin, players_candies, comp_candies, \
        first_turn_fail, select_game_mode, candies_count, candies_take, game_mode
    candies = 150
    max_candies_in_round = 28
    coin = -1
    players_candies = 0
    comp_candies = 0
    first_turn_fail = False
    select_game_mode = False
    candies_count = False
    candies_take = False
    game_mode = 1
    print(message.text)
    print(message.from_user.id)
    print(message.from_user.first_name)
    await bot.send_message(message.from_user.id,
                           f'Ну что, {message.from_user.first_name}, сыграем в конфеты? '
                           f'У меня на столе лежит {candies} конфет. '
                           f'За один ход ты можешь взять от 1 до {max_candies_in_round} конфет. '
                           f'Кто заберет последние конфеты, тот и выиграл. '
                           f'Введи команду /roll для определения очередности хода. '
                           f'1 - ходишь первым ты, 0 - я.'
                           f'Чтобы узнать список всех команд введи /help')


async def help(message: types.Message):
    await bot.send_message(message.from_user.id,
                           '/start - начать новую игру\n'
                           '/roll - определить очередность хода\n'
                           '/mode - выбор уровня сложности\n'
                           '/count - изменить количество конфет на столе\n'
                           '/take - изменить максимальное количество конфет, '
                           'которое можно взять за 1 ход')


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
                               f'Твоя очередь ходить! '
                               f'Возьми от 1 до {max_candies_in_round} конфет.')
    else:
        await bot.send_message(message.from_user.id,
                               'Повезло! Ходи первым!')


async def mode(message: types.Message):
    global select_game_mode, candies_count, candies_take
    candies_count = False
    candies_take = False
    select_game_mode = True
    await bot.send_message(message.from_user.id,
                           'Выбери режим: 0 - легко, 1 - сложно')


async def count(message: types.Message):
    global select_game_mode, candies_count, candies_take
    select_game_mode = False
    candies_take = False
    candies_count = True
    await bot.send_message(message.from_user.id,
                           'Введи количество конфет на столе')


async def take(message: types.Message):
    global select_game_mode, candies_count, candies_take
    select_game_mode = False
    candies_count = False
    candies_take = True
    await bot.send_message(message.from_user.id,
                           'Введи максимальное количество конфет, '
                           'которое можно взять за 1 ход')


async def anything(message: types.Message):
    global coin, candies, players_candies, first_turn_fail, comp_candies, \
        max_candies_in_round, select_game_mode, candies_count, candies_take, game_mode
    if message.text.isdigit():

        if candies_count and int(message.text) > max_candies_in_round:
            candies = int(message.text)
            candies_count = False
            await bot.send_message(message.from_user.id,
                                   f'Отлично! Теперь на столе лежит {candies} конфет!')

        elif candies_count and int(message.text) <= max_candies_in_round:
            await bot.send_message(message.from_user.id,
                                   'Количество конфет на столе меньше или равно количеству конфет, '
                                   'которое можно взять за 1 ход. Введи другое значение')

        elif candies_take and int(message.text) < candies:
            max_candies_in_round = int(message.text)
            candies_take = False
            await bot.send_message(message.from_user.id,
                                   f'Отлично! Теперь за 1 ход можно взять '
                                   f'{max_candies_in_round} конфет!')

        elif candies_take and int(message.text) >= candies:
            await bot.send_message(message.from_user.id,
                                   'Количество конфет на столе меньше или равно количеству конфет, '
                                   'которое можно взять за 1 ход. Введи другое значение')

        elif select_game_mode:
            if int(message.text) == 1:
                game_mode = 1
                select_game_mode = False
                await bot.send_message(message.from_user.id,
                                       'Выбран сложный режим игры')
            elif int(message.text) == 0:
                game_mode = 0
                select_game_mode = False
                await bot.send_message(message.from_user.id,
                                       'Выбран легкий режим игры')
            else:
                await bot.send_message(message.from_user.id,
                                       'Надо выбрать 0 или 1')

        else:
            if game_mode == 1:
                if coin == -1:
                    await bot.send_message(message.from_user.id,
                                           'Не торопись! Сначала нужно определить очередность хода!')
                else:
                    if candies > 0:
                        players_candies = int(message.text)
                        if players_candies < 1 or players_candies > max_candies_in_round:
                            await bot.send_message(message.from_user.id,
                                                   f'В задании же сказано от 1 до {max_candies_in_round} конфет! '
                                                   f'Вводи заново!')

                        else:
                            candies -= players_candies
                            if candies <= 0:
                                await bot.send_message(message.from_user.id,
                                                       'Поздравляю! Ты выиграл! Все конфеты твои! '
                                                       'Чтобы начать новую игру введи /start')
                            else:
                                await bot.send_message(message.from_user.id,
                                                       f'Ты взял {players_candies} конфет. '
                                                       f'Осталось {candies} конфет! Моя очередь ходить!')

                                if first_turn_fail:
                                    comp_candies = candies % (max_candies_in_round + 1)
                                    if comp_candies > candies:
                                        comp_candies = candies
                                        candies = 0
                                        await bot.send_message(message.from_user.id,
                                                               f'Я взял {comp_candies} конфет! Конфет не осталось! '
                                                               f'Я выиграл! Чтобы начать новую игру введи /start')
                                    elif comp_candies == 0 or comp_candies > max_candies_in_round:
                                        comp_candies = 1
                                        first_turn_fail = True
                                    else:
                                        first_turn_fail = False
                                    candies -= comp_candies

                                    await bot.send_message(message.from_user.id,
                                                           f'Я взял {comp_candies} конфет! Осталось {candies}! '
                                                           f'Твоя очередь ходить!')

                                elif (candies > (max_candies_in_round * 2)) or (candies == max_candies_in_round + 1):
                                    comp_candies = max_candies_in_round + 1 - players_candies
                                    candies -= comp_candies
                                    await bot.send_message(message.from_user.id,
                                                           f'Я взял {comp_candies} конфет! Осталось {candies}! '
                                                           f'Твоя очередь ходить!')

                                elif (max_candies_in_round + 1) < candies < (max_candies_in_round * 2 + 1):
                                    comp_candies = candies - max_candies_in_round - 1
                                    candies -= comp_candies
                                    await bot.send_message(message.from_user.id,
                                                           f'Я взял {comp_candies} конфет! Осталось {candies}! '
                                                           f'Твоя очередь ходить!')

                                else:
                                    comp_candies = candies
                                    candies = 0
                                    await bot.send_message(message.from_user.id,
                                                           f'Я взял {comp_candies} конфет! Конфет не осталось! Я выиграл! '
                                                           f'Чтобы начать новую игру введи /start')

                    else:
                        await bot.send_message(message.from_user.id,
                                               'Игра окончена! Чтобы начать новую игру введи /start')

            else:
                if game_mode == 0:
                    if coin == -1:
                        await bot.send_message(message.from_user.id,
                                               'Не торопись! Сначала нужно определить очередность хода!')
                    else:
                        if candies > 0:
                            players_candies = int(message.text)
                            if players_candies < 1 or players_candies > max_candies_in_round:
                                await bot.send_message(message.from_user.id,
                                                       f'В задании же сказано от 1 до {max_candies_in_round} конфет! '
                                                       f'Вводи заново!')

                            else:
                                candies -= players_candies
                                if candies <= 0:
                                    await bot.send_message(message.from_user.id,
                                                           'Поздравляю! Ты выиграл! Все конфеты твои! '
                                                           'Чтобы начать новую игру введи /start')
                                else:
                                    await bot.send_message(message.from_user.id,
                                                           f'Ты взял {players_candies} конфет. '
                                                           f'Осталось {candies} конфет! Моя очередь ходить!')

                                    if (candies > (max_candies_in_round * 2)) or (
                                            candies == max_candies_in_round + 1):
                                        comp_candies = random.randint(1, max_candies_in_round)
                                        candies -= comp_candies
                                        await bot.send_message(message.from_user.id,
                                                               f'Я взял {comp_candies} конфет! Осталось {candies}! '
                                                               f'Твоя очередь ходить!')

                                    elif (max_candies_in_round + 1) < candies < (max_candies_in_round * 2 + 1):
                                        comp_candies = candies - max_candies_in_round - 1
                                        candies -= comp_candies
                                        await bot.send_message(message.from_user.id,
                                                               f'Я взял {comp_candies} конфет! Осталось {candies}! '
                                                               f'Твоя очередь ходить!')

                                    else:
                                        comp_candies = candies
                                        candies = 0
                                        await bot.send_message(message.from_user.id,
                                                               f'Я взял {comp_candies} конфет! '
                                                               f'Конфет не осталось! Я выиграл! '
                                                               f'Чтобы начать новую игру введи /start')

                        else:
                            await bot.send_message(message.from_user.id,
                                                   'Игра окончена! Чтобы начать новую игру введи /start')
    else:
        await bot.send_message(message.from_user.id,
                               'Я букв не знаю, давай цифры')
