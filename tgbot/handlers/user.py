from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline import *
from tgbot.models.sql_connector import *
from tgbot.misc.states import FSMUser
from tgbot.misc.calculator import calculator, rounder
from create_bot import bot

import math


async def user_start_msg(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    is_user = await check_user_sql(user_id)
    if not is_user:
        await create_user_sql(user_id, username)
    text = [
        'Введите два числа через пробел или посмотрите свои операции. Числа можно вводить как через точку, так и',
        'через запятую'
    ]
    kb = static_kb()
    await FSMUser.home.set()
    await message.answer(' '.join(text), reply_markup=kb)


async def user_start_clb(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    is_user = await check_user_sql(user_id)
    if not is_user:
        await create_user_sql(user_id, username)
    text = [
        'Введите два числа через пробел или посмотрите свои операции. Числа можно вводить как через точку, так и',
        'через запятую'
    ]
    kb = static_kb()
    await FSMUser.home.set()
    await callback.message.answer(' '.join(text), reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def get_numbers(message: Message, state: FSMContext):
    numbers = message.text.split()
    if len(numbers) != 2:
        text = 'Необходимо ввести 2 числа через пробел'
        kb = home_kb()
    else:
        try:
            num1 = float(numbers[0].replace(',', '.'))
            num2 = float(numbers[1].replace(',', '.'))
            async with state.proxy() as data:
                data['num1'] = num1
                data['num2'] = num2
            text = 'Выберите операцию'
            kb = operations_kb()
            await FSMUser.numbers.set()
        except:
            text = 'Вы ввели не числа'
            kb = home_kb()
    await message.answer(text, reply_markup=kb)


async def result(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    async with state.proxy() as data:
        num1 = data.as_dict()['num1']
        num2 = data.as_dict()['num2']
    operator = callback.data.split(':')[1]
    if num2 == 0 and operator == '/':
        text = 'Делить на ноль нельзя'
    else:
        res_list = await calculator(num1, num2, operator)
        operation = f'{res_list[0]}{operator}{res_list[1]}'
        text = f'<b><i>Результат:</i></b>\n{operation}={res_list[2]}'
        await FSMUser.home.set()
        await create_operation_sql(user_id, operation, res_list[2])
    kb = home_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def static(callback: CallbackQuery):
    user_id = callback.from_user.id
    operations = await get_static_sql(user_id)
    if len(operations) == 0:
        text = ['Вы не совершали рассчётов']
    else:
        text = ['<b><i>Ваши рассчёты:</i></b>']
        for operation in operations:
            res = await rounder([operation['result']])
            row = f'{operation["operation"]}={res[0]}'
            text.append(row)
    kb = home_kb()
    await callback.message.answer('\n'.join(text), reply_markup=kb)
    await bot.answer_callback_query(callback.id)



def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start_msg, commands=["start"], state="*")
    dp.register_message_handler(get_numbers, content_types='text', state=FSMUser.home)

    dp.register_callback_query_handler(user_start_clb, lambda x: x.data == 'home', state='*')
    dp.register_callback_query_handler(result, lambda x: x.data.split(':')[0] == 'sign', state=FSMUser.numbers)
    dp.register_callback_query_handler(static, lambda x: x.data == 'static', state='*')

