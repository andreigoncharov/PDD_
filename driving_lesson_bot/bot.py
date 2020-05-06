import asyncio
from aiogram import Bot, Dispatcher, executor
import scripts.messages as msg
#import scripts.google_drive
import scripts.markup as mk
from config import TOKEN
import scripts.search as search
from scripts.db_manager import UsersDbManager
import uuid
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, ContentType
import aiogram
import random
from scripts.dict_w import Work as wk
import config
import datetime
import aiogram.types as tp
import detection.det as dt
from keras.models import load_model
import requests
from io import BytesIO

bot = Bot(TOKEN)
dp = Dispatcher(bot)

loop = asyncio.get_event_loop()

#model = load_model('traffic_recognition.h5')

href_pdr = 'https://vodiy.ua/ru/pdr/'
href_tabl = 'https://vodiy.ua/ru/znaky/'
href_razm = 'https://vodiy.ua/ru/rozmitka/'


@dp.message_handler(commands=['start'])
async def start(message):
    tel_id = message.chat.id
    username = message.from_user.username
    name = message.from_user.first_name

    if not await UsersDbManager.user_exist(tel_id, loop):
        await UsersDbManager.add_user(tel_id, username, '0', loop)
    user = await UsersDbManager.get_user(tel_id, loop)

    text = msg.greeting.format(name)
    keyboard = mk.main_menu_ru

    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)


@dp.message_handler(lambda message: message.text == '⬅️ Назад')
async def to_main_menu(message):
    tel_id = message.chat.id
    user = await UsersDbManager.get_user(tel_id, loop)

    keyboard = mk.main_menu_ru
    text = 'Главное меню'

    await UsersDbManager.update_context(tel_id, '0', loop)
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)

'''
Теория
'''

@dp.message_handler(lambda message:
                    message.text == 'Почитать теорию')
async def read_theory(message):
    tel_id = message.chat.id
    user = await UsersDbManager.get_user(tel_id, loop)

    nums = await UsersDbManager.get_pp(tel_id,loop)
    if nums[0] == 0 and nums[1]==0:
        text = msg.category
        keyboard = mk.theory_category
        await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)

    else:
        text = 'Хотите продолжить чтение теории с того места, где Вы остановились?'
        keyboard = mk.yes_or_no()
        await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)


@dp.message_handler(lambda message: message.text == 'Дорожные знаки и таблички')
async def tabl(message):
    tel_id = message.chat.id
    keyboard = mk.show_cat()
    text = msg.category
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)

@dp.message_handler(lambda message:
                    message.text == 'Дорожная разметка')
async def razm(message):
    print(1)
    tel_id = message.chat.id
    keyboard = mk.show_cat_razm()
    text = msg.category
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)

'''
Продолжить чтение теории
'''
@dp.callback_query_handler(lambda call:
                           call.data.startswith('cont_yes'))
async def count_yes(call):
    tel_id = call.message.chat.id
    nums = await UsersDbManager.get_pp(tel_id, loop)
    num = nums[1]
    w = await search.get_count(nums[0])
    if num <= w:
        if nums[0] == 1 and num == 10:
            text = f"Пункт {nums[0]}.{num}\n" + 'Термины ПДД:\nhttps://telegra.ph/Terminy-privedennye-v-ehtih-Pravilah-imeyut-sleduyushchee-znachenie-11-27'
            keyboard = mk.next_back()
            await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
            num += 1
            await UsersDbManager.update_pp(tel_id, nums[0], num, loop)
        else:
            text = f"Пункт {nums[0]}.{num}\n" + str(await search.main_to_text(nums[0], num))
            keyboard = mk.next_back()
            await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
            num += 1
            await UsersDbManager.update_pp(tel_id, nums[0], num, loop)
    elif num > w:
        await bot.edit_message_text('Вы прочитали все пункты в этом разделе. Переходите к следующим разделам!', tel_id,
                                    call.message.message_id, reply_markup=mk.show_pdd_cat())

@dp.callback_query_handler(lambda call:
                           call.data.startswith('cont_no'))
async def count_no(call):
    tel_id = call.message.chat.id
    text = msg.category
    keyboard = mk.theory_category
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)
'''
---------------------------------
'''

'''
Категория: ПДД
Выбор и чтение ПДД согласно с выбранной категорией
'''

@dp.message_handler(lambda message:
                    message.text == 'Правила дорожного движения')
async def pdd1(message):
    tel_id = message.chat.id
    keyboard = mk.show_pdd_cat()
    text = msg.category
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)

@dp.callback_query_handler(lambda call: call.data.startswith('show_pdd_cat'))
async def show_pdd_cat(call):
    tel_id = call.message.chat.id
    keyboard = mk.show_pdd_cat()
    text = msg.category
    await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith('to_pdd_2'))
async def pdd2(call):
    tel_id = call.message.chat.id
    keyboard = mk.to_pdd_2()
    text = msg.category
    await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith('to_pdd_3'))
async def pdd3(call):
    tel_id = call.message.chat.id
    keyboard = mk.to_pdd_3()
    text = msg.category
    await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith('to_pdd_4'))
async def pdd4(call):
    tel_id = call.message.chat.id
    keyboard = mk.to_pdd_4()
    text = msg.category
    await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith('to_menu'))
async def to_menu(call):
    tel_id = call.message.chat.id
    keyboard = mk.main_menu_ru
    text = msg.main_menu
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)
    await bot.delete_message(tel_id, call.message.message_id)


@dp.message_handler(lambda message:
                    message.text == 'show')
async def test_start(message):
    tel_id = message.chat.id
    p = await UsersDbManager.sel(loop)
    await bot.send_message(tel_id, p[1], disable_notification=True)
    await bot.send_photo(tel_id, p[5])

'''
Прохождение теста
'''
@dp.message_handler(lambda message:
                    message.text == 'Пройти тест')
async def start_test(message):
    tel_id = message.chat.id
    text = msg.start_test
    keyboard = mk.test_keyboard
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)

@dp.message_handler(lambda message:
                    message.text == 'Мои результаты')
async def start_test(message):
    tel_id = message.chat.id
    results = await UsersDbManager.history(tel_id, loop)
    res= results[0]
    count = res[1]
    count_s = res[2]
    count_e = res[3]
    text = f'☑ Общее количество\nпройденных тестов: {count}\n🔘Количество успешно\nпройденных тестов: {count_s}\n🔘Количество не пройденных тестов:{count_e}'
    keyboard = mk.main_menu_ru
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)

'''
Категория: Тест по темам
Выбор темы
'''

@dp.message_handler(lambda message:
                    message.text == msg.test_keyboard[0])
async def test_1(message):
    tel_id = message.chat.id
    text = 'Выбери тему'
    keyboard = mk.test_category
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)

@dp.message_handler(lambda message:
                    message.text == msg.test_category[0])
async def test_1_1(message):
    tel_id = message.chat.id
    text = msg.selected_test.format(msg.test_category[0])
    keyboard = mk.start_close
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)
    await UsersDbManager.update_context(tel_id, 'test_1', loop)

@dp.message_handler(lambda message:
                    message.text == msg.test_category[1])
async def test_1_2(message):
    tel_id = message.chat.id
    text = msg.selected_test.format(msg.test_category[1])
    keyboard = mk.start_close
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)
    await UsersDbManager.update_context(tel_id, 'test_2', loop)

@dp.message_handler(lambda message:
                    message.text == msg.test_category[2])
async def test_1_3(message):
    tel_id = message.chat.id
    text = msg.selected_test.format(msg.test_category[2])
    keyboard = mk.start_close
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)
    await UsersDbManager.update_context(tel_id, 'test_3', loop)

'''
Категория: Случайные вопросы
'''

@dp.message_handler(lambda message:
                    message.text == msg.test_keyboard[1])
async def tes__t_2(message):
    tel_id = message.chat.id
    keyboard = mk.start
    text = 'ℹ️ Вы выбрали случайные вопросы\n' \
    f'⏱ Время пойдет после того, как нажмете кнопку "Начать"\n' \
    f'Удачи 😉'
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)


'''
Начало или отмена теста
'''
def get_index(d):
    k_l = list(d.keys())
    ind = k_l.index(1)
    if ind == 0:
        print('A')
        return 'A'
    elif ind == 1:
        print('B')
        return 'B'
    elif ind == 2:
        print('C')
        return 'C'
    elif ind == 3:
        print('D')
        return 'D'
    elif ind == 4:
        print('E')
        return 'E'

@dp.message_handler(lambda message:
                    message.text == msg.start[0])
async def test_t(message):
    text = ''
    q_list = []
    answ = []
    r_answ = ''
    img = ''
    tel_id = message.chat.id
    q_list = await UsersDbManager.get_rand_q(loop)
    nums = []
    for q in q_list:
        nums.append(q)
    p = nums[0]
    nums.remove(p)
    nums = sorted(nums, key=lambda A: random.random())
    await UsersDbManager.add_to_q(tel_id, nums, loop)
    quest = q_list[0]
    text = quest[2]
    s = str(quest[3])
    answ.append(s.split('/'))
    r_answ = quest[4]
    img = quest[5]
    message = ''
    answ = answ[0]
    answ = sorted(answ, key=lambda A: random.random())
    r_dict ={}
    k_l = []
    if len(answ) + 1 == 2:
        d = {1: r_answ, 2: answ[0]}
        r_dict = wk.shuffle_dict(d)
        print(r_dict)
        d.clear()
        r_index = get_index(r_dict)
        await UsersDbManager.update_right_answer(tel_id, r_index, loop)
        message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}'
    elif len(answ) + 1 == 3:
        d = {1: r_answ, 2: answ[0], 3: answ[1]}
        r_dict = wk.shuffle_dict(d)
        print(r_dict)
        d.clear()
        r_index = get_index(r_dict)
        await UsersDbManager.update_right_answer(tel_id, r_index, loop)
        message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}'
    elif len(answ) + 1 == 4:
        d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2]}
        r_dict = wk.shuffle_dict(d)
        print(r_dict)
        d.clear()
        r_index = get_index(r_dict)
        await UsersDbManager.update_right_answer(tel_id, r_index, loop)
        message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n 🔘D- {list(r_dict.items())[3][1]}'
    elif len(answ) + 1 == 5:
        d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2], 5:answ[3]}
        r_dict = wk.shuffle_dict(d)
        print(r_dict)
        d.clear()
        r_index = get_index(r_dict)
        await UsersDbManager.update_right_answer(tel_id, r_index, loop)
        message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n 🔘D- {list(r_dict.items())[3][1]}\n 🔘E- {list(r_dict.items())[4][1]}'

    if len(img) != 0:
        await bot.send_photo(tel_id, img, disable_notification=True)
        await bot.send_message(tel_id, message, reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list= r_dict.keys()),
                               disable_notification=True)
    else:
        await bot.send_message(tel_id, message, reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list= r_dict.keys()),
                               disable_notification=True)


@dp.message_handler(lambda message:
                    message.text == msg.start_close[0])
async def test_start(message):
    tel_id = message.chat.id
    text = ''
    context = await UsersDbManager.get_context(tel_id, loop)
    q_list = []
    answ=[]
    r_answ=''
    img=''
    if context == 'test_1':
        nums = []
        q_list = await UsersDbManager.get_q(1, loop)
        for q in q_list:
            nums.append(q)
        p = nums[0]
        nums.remove(p)
        nums = sorted(nums, key=lambda A: random.random())
        await UsersDbManager.add_to_q(tel_id, nums, loop)
        quest = q_list[0]
        text = quest[2]
        s = str(quest[3])
        answ.append(s.split('/'))
        r_answ = quest[4]
        img = quest[5]
        message =''
        answ = answ[0]
        answ = sorted(answ, key=lambda A: random.random())
        r_dict = {}
        if len(answ) + 1 == 2:
            d = {1: r_answ, 2: answ[0]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}'
        elif len(answ) + 1 == 3:
            d = {1: r_answ, 2: answ[0], 3: answ[1]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}'
        elif len(answ) + 1 == 4:
            d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n 🔘D- {list(r_dict.items())[3][1]}'
        elif len(answ) + 1 == 5:
            d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2], 5: answ[3]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n 🔘D- {list(r_dict.items())[3][1]}\n 🔘E- {list(r_dict.items())[4][1]}'

        if len(img) != 0:
            await bot.send_photo(tel_id, img, disable_notification=True)
            await bot.send_message(tel_id, message,
                                   reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list=r_dict.keys()),
                                   disable_notification=True)
        else:
            await bot.send_message(tel_id, message,
                                   reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list=r_dict.keys()),
                                   disable_notification=True)


    elif context == 'test_2':
        nums = []
        q_list = await UsersDbManager.get_q(2, loop)
        for q in q_list:
            nums.append(q)
        p = nums[0]
        nums.remove(p)
        nums = sorted(nums, key=lambda A: random.random())
        await UsersDbManager.add_to_q(tel_id, nums, loop)
        quest = q_list[0]
        text = quest[2]
        s = str(quest[3])
        answ.append(s.split('/'))
        r_answ = quest[4]
        img = quest[5]
        message = ''
        answ = answ[0]
        answ = sorted(answ, key=lambda A: random.random())
        r_dict = {}
        if len(answ) + 1 == 2:
            d = {1: r_answ, 2: answ[0]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}'
        elif len(answ) + 1 == 3:
            d = {1: r_answ, 2: answ[0], 3: answ[1]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}'
        elif len(answ) + 1 == 4:
            d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n 🔘D- {list(r_dict.items())[3][1]}'
        elif len(answ) + 1 == 5:
            d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2], 5: answ[3]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n 🔘D- {list(r_dict.items())[3][1]}\n 🔘E- {list(r_dict.items())[4][1]}'

        if len(img) != 0:
            await bot.send_photo(tel_id, img, disable_notification=True)
            await bot.send_message(tel_id, message,
                                   reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list=r_dict.keys()),
                                   disable_notification=True)
        else:
            await bot.send_message(tel_id, message,
                                   reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list=r_dict.keys()),
                                   disable_notification=True)
    elif context == 'test_3':
        nums = []
        q_list = await UsersDbManager.get_q(3, loop)
        for q in q_list:
            nums.append(q)
        p = nums[0]
        nums.remove(p)
        nums = sorted(nums, key=lambda A: random.random())
        await UsersDbManager.add_to_q(tel_id, nums, loop)
        quest = q_list[0]
        text = quest[2]
        s = str(quest[3])
        answ.append(s.split('/'))
        r_answ = quest[4]
        img = quest[5]
        message = ''
        answ = answ[0]
        answ = sorted(answ, key=lambda A: random.random())
        r_dict = {}
        if len(answ) + 1 == 2:
            d = {1: r_answ, 2: answ[0]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}'
        elif len(answ) + 1 == 3:
            d = {1: r_answ, 2: answ[0], 3: answ[1]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}'
        elif len(answ) + 1 == 4:
            d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n 🔘D- {list(r_dict.items())[3][1]}'
        elif len(answ) + 1 == 5:
            d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2], 5: answ[3]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n ' \
                      f'🔘D- {list(r_dict.items())[3][1]}\n 🔘E- {list(r_dict.items())[4][1]}'

        if len(img) != 0:
            await bot.send_photo(tel_id, img, disable_notification=True)
            await bot.send_message(tel_id, message,
                                   reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list=r_dict.keys()),
                                   disable_notification=True)
        else:
            await bot.send_message(tel_id, message,
                                   reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list=r_dict.keys()),
                                   disable_notification=True)
    else :
        print(12321)
        await UsersDbManager.get_rand_q(loop)


@dp.callback_query_handler(lambda call: call.data.startswith('right'))
async def show_img(call):
    tel_id = call.message.chat.id
    q_list = []
    answ = []
    r_answ = ''
    img = ''
    d = {}
    num, count, time, errors, r_a = await UsersDbManager.for_new_q(tel_id, loop)
    time = float(time)
    if count >0:
        print('num = ',num)
        q_list = await UsersDbManager.new_q(num, loop)
        q_list = list(q_list)
        q_list = q_list[0]
        text = q_list[2]
        s = str(q_list[3])
        answ.append(s.split('/'))
        r_answ = q_list[4]
        img = q_list[5]
        message = ''
        answ = answ[0]
        answ = sorted(answ, key=lambda A: random.random())

        message_id = call.message.message_id
        message_text = call.message.text + '\n\n ✅ ______________________________________ ✅ \n' + f'\n 🟢 Вы правильно ответили на вопрос!\n' \
                                                                                                 f'\n 🔠 Осталось вопросов: {count}\n ⏱ Осталось времени: {round(20 - time)} минут\n' \
                                                                                                 f'❗️Допущено ошибок: {errors}\n' + '\n ✅ ______________________________________ ✅ \n'
        await bot.delete_message(tel_id, message_id)
        await bot.send_message(tel_id, message_text, disable_notification=True)
        r_dict = {}
        if len(answ) + 1 == 2:
            d = {1: r_answ, 2: answ[0]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}'
        elif len(answ) + 1 == 3:
            d = {1: r_answ, 2: answ[0], 3: answ[1]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}'
        elif len(answ) + 1 == 4:
            d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n 🔘D- {list(r_dict.items())[3][1]}'
        elif len(answ) + 1 == 5:
            d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2], 5: answ[3]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n ' \
                      f'🔘D- {list(r_dict.items())[3][1]}\n 🔘E- {list(r_dict.items())[4][1]}'

        if len(img) != 0:
            await bot.send_photo(tel_id, img, disable_notification=True)
            await bot.send_message(tel_id, message,
                                   reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list=r_dict.keys()),
                                   disable_notification=True)
        else:
            await bot.send_message(tel_id, message,
                                   reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list=r_dict.keys()),
                                   disable_notification=True)
    else:
        f_text = ''
        if errors <= 2:
            f_text = f'Поздравляем!\nВы успешно прошли тест!\n☑️Количество ошибок: {errors}\n☑️Количество потраченного времени: {round(20-(20 - time))} мин.'
            await UsersDbManager.update_context(tel_id, '', loop)
            await UsersDbManager.update_history_s(tel_id, loop)
            UsersDbManager.clear_test(tel_id)
        else:
            f_text = f'Тест окончен.\n К сожалению Bы не прошли тест, так как количество Bаших ошибок - {errors}(допустимое количество ошибок - 2).\n' \
                     f'Но не расстраивайтесь, подучите теорию и попробуйте еще раз😉\n У вас все получится!'
            await UsersDbManager.update_context(tel_id, '', loop)
            await UsersDbManager.update_history_e(tel_id, loop)
            UsersDbManager.clear_test(tel_id)
        await bot.send_message(tel_id, f_text, reply_markup=mk.main_menu_ru, disable_notification=True)


@dp.callback_query_handler(lambda call: call.data.startswith('wrong'))
async def show_img(call):
    tel_id = call.message.chat.id
    q_list = []
    answ = []
    r_answ = ''
    img = ''
    d = {}
    num, count, time, errors, right_answer = await UsersDbManager.for_new_q(tel_id, loop)
    time = float(time)
    if count > 0:
        await UsersDbManager.update_errors(tel_id, loop)
        print('num = ', num)
        q_list = await UsersDbManager.new_q(num, loop)
        q_list = list(q_list)
        q_list = q_list[0]
        text = q_list[2]
        s = str(q_list[3])
        answ.append(s.split('/'))
        r_answ = q_list[4]
        img = q_list[5]
        message = ''
        answ = answ[0]
        answ = sorted(answ, key=lambda A: random.random())
        message_id = call.message.message_id
        message_text = call.message.text + '\n\n ❌ ______________________________________ ❌ \n\n'+ f' 🛑 Вы не правильно ответили на вопрос!\n' \
                                                                                                   f'\n ✅ Правильный ответ: {right_answer}\n' \
                                                                                                   f' 🔠 Осталось вопросов: {count}\n' \
                                                                                                   f' ⏱ Осталось времени: {round(20 - time)} мин\n' \
                                                                                                   f'❗️Допущено ошибок: {errors+1}\n' + '\n ❌ ______________________________________ ❌ \n\n'
        await bot.delete_message(tel_id, message_id)
        await bot.send_message(tel_id, message_text, disable_notification=True)
        r_dict = {}
        if len(answ) + 1 == 2:
            d = {1: r_answ, 2: answ[0]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}'
        elif len(answ) + 1 == 3:
            d = {1: r_answ, 2: answ[0], 3: answ[1]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}'
        elif len(answ) + 1 == 4:
            d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n 🔘D- {list(r_dict.items())[3][1]}'
        elif len(answ) + 1 == 5:
            d = {1: r_answ, 2: answ[0], 3: answ[1], 4: answ[2], 5: answ[3]}
            r_dict = wk.shuffle_dict(d)
            print(r_dict)
            d.clear()
            r_index = get_index(r_dict)
            await UsersDbManager.update_right_answer(tel_id, r_index, loop)
            message = f'{text}\n 🔘A- {list(r_dict.items())[0][1]}\n 🔘B- {list(r_dict.items())[1][1]}\n 🔘C- {list(r_dict.items())[2][1]}\n 🔘D- {list(r_dict.items())[3][1]}\n 🔘E- {list(r_dict.items())[4][1]}'

        if len(img) != 0:
            await bot.send_photo(tel_id, img, disable_notification=True)
            await bot.send_message(tel_id, message,
                                   reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list=r_dict.keys()),
                                   disable_notification=True)
        else:
            await bot.send_message(tel_id, message,
                                   reply_markup=mk.get_test_keyboard(len(answ) + 1, keys_list=r_dict.keys()),
                                   disable_notification=True)
    else:
        f_text = ''
        if errors <= 2:
            f_text = f'Поздравляем!\nВы успешно прошли тест!\n☑️Количество ошибок: {errors}\n☑️Количество потраченного времени: {round(20-(20 - time))} мин.'
            await UsersDbManager.update_context(tel_id, '', loop)
            await UsersDbManager.update_history_s(tel_id, loop)
            UsersDbManager.clear_test(tel_id)
        else:
            f_text = f'Тест окончен.\n К сожалению вы не прошли тест, так как количество ваших ошибок - {errors}(допустимое количество ошибок - 2).\nНо не расстраивайтесь, подучите теорию и попробуйте еще раз😉\n У вас все получится!'
            await UsersDbManager.update_context(tel_id, '', loop)
            await UsersDbManager.update_history_e(tel_id, loop)
            UsersDbManager.clear_test(tel_id)
        await bot.send_message(tel_id, f_text, reply_markup=mk.main_menu_ru, disable_notification=True)

@dp.message_handler(lambda message:
                    message.text == msg.start_close[1])
async def test_close(message):
    tel_id = message.chat.id
    text = 'Главное меню'
    keyboard = mk.main_menu_ru
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)


@dp.callback_query_handler(lambda call:
                           call.data.startswith('pred_zn') or
                           call.data.startswith('pr_zn') or
                           call.data.startswith('zapr_zn') or
                           call.data.startswith('uk_zn') or
                           call.data.startswith('i-u_zn') or
                           call.data.startswith('zn_serv') or
                           call.data.startswith('tabl_zn'))
async def _cat_2(call):
    tel_id = call.message.chat.id
    text = 'Категория: '
    if call.data == 'pred_zn':
        text += 'Предупреждающие знаки'
    elif call.data == 'pr_zn':
        text += 'Знаки приоритета'
    elif call.data == 'zapr_zn':
        text += 'Запрещающие знаки'
    elif call.data == 'uk_zn':
        text += 'Указательные знаки'
    elif call.data == 'i-u_zn':
        text += 'Информационно-указательные знаки'
    elif call.data == 'zn_serv':
        text += 'Знаки сервиса'
    elif call.data == 'tabl_zn':
        text += 'Таблички к дорожным знакам'
    text += '\nНапишите вопрос'

    await bot.send_message(tel_id, text, disable_notification=True)


@dp.callback_query_handler(lambda call:
                           call.data.startswith('tabl_1') or
                           call.data.startswith('tabl_2'))
async def _cat_3(call):
    tel_id = call.message.chat.id
    text = 'Категория: '
    if call.data == 'tabl_1':
        text += 'Горизонтальная разметка'
    elif call.data == 'tabl_2':
        text += 'Вертикальная разметка'
    text += '\nНапишите вопрос'

    await bot.send_message(tel_id, text, disable_notification=True)

@dp.callback_query_handler(lambda call:
                           call.data.startswith('/back_cat'))
async def _back(call):
    tel_id = call.message.chat.id
    keyboard = mk.get_cat_keyboard()
    text = 'Категория:'
    await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)

@dp.callback_query_handler(lambda call:
                           call.data.startswith('show_p_1') or
                           call.data.startswith('show_p_2') or
                           call.data.startswith('show_p_3') or
                           call.data.startswith('show_p_4') or
                           call.data.startswith('show_p_5') or
                           call.data.startswith('show_p_6') or
                           call.data.startswith('show_p_7') or
                           call.data.startswith('show_p_8'))
async def _back(call):
    tel_id = call.message.chat.id
    keyboard = mk.next_back()
    number = call.data[7:]
    text = ''
    if call.data == 'show_p_1':
        text = f"Пункт {number}.1\n"+ str(await search.main_to_text(number, 1))
        await UsersDbManager.update_pp(tel_id, number, 2, loop)
    elif call.data == 'show_p_2':
        text = f"Пункт {number}.1\n"+ str(await search.main_to_text(number, 1))
        await UsersDbManager.update_pp(tel_id, number, 2, loop)
    elif call.data == 'show_p_3':
        text = f"Пункт {number}.1\n"+ str(await search.main_to_text(number, 1))
        await UsersDbManager.update_pp(tel_id, number, 2, loop)
    elif call.data == 'show_p_4':
        text = f"Пункт {number}.1\n"+ str(await search.main_to_text(number, 1))
        await UsersDbManager.update_pp(tel_id, number, 2, loop)
    elif call.data == 'show_p_5':
        text = f"Пункт {number}.1\n"+ str(await search.main_to_text(number, 1))
        await UsersDbManager.update_pp(tel_id, number, 2, loop)
    elif call.data == 'show_p_6':
        text = f"Пункт {number}.1\n"+ str(await search.main_to_text(number, 1))
        await UsersDbManager.update_pp(tel_id, number, 2, loop)
    elif call.data == 'show_p_7':
        text = f"Пункт {number}.1\n"+ str(await search.main_to_text(number, 1))
        await UsersDbManager.update_pp(tel_id, number, 2, loop)
    elif call.data == 'show_p_8':
        text =f"Пункт {number}.1\n"+  str(await search.main_to_text(number, 1))
        await UsersDbManager.update_pp(tel_id, number, 2, loop)
    await bot.send_message(tel_id, text, reply_markup=keyboard)
    await bot.delete_message(call.message.chat.id, call.message.message_id)

@dp.callback_query_handler(lambda call:
                           call.data.startswith('show_pp_9') or
                           call.data.startswith('show_pp_0') or
                           call.data.startswith('show_pp_1') or
                           call.data.startswith('show_pp_2') or
                           call.data.startswith('show_pp_3') or
                           call.data.startswith('show_pp_4') or
                           call.data.startswith('show_pp_5') or
                           call.data.startswith('show_pp_6') or
                           call.data.startswith('show_pp_7') or
                           call.data.startswith('show_pp_8') or
                           call.data.startswith('show_pp_9'))
async def _back(call):
    tel_id = call.message.chat.id
    keyboard = mk.next_back()
    number = call.data[8:]
    text = ''
    if call.data == 'show_pp_9':
        text = f"Пункт {number}.1\n"+ str(await search.main_to_text(number, 1))
        await UsersDbManager.update_pp(tel_id, number, 2, loop)
    elif call.data == 'show_pp_0':
        text = f"Пункт {int(number) + 10}.1\n"+str(await search.main_to_text(int(number) + 10, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 10, 2, loop)
    elif call.data == 'show_pp_1':
        text = f"Пункт {int(number) + 10}.1\n"+str(await search.main_to_text(int(number) + 10, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 10, 2, loop)
    elif call.data == 'show_pp_2':
        text = f"Пункт {int(number) + 10}.1\n"+ str(await search.main_to_text(int(number) + 10, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 10, 2, loop)
    elif call.data == 'show_pp_3':
        text = f"Пункт {int(number) + 10}.1\n"+str(await search.main_to_text(int(number) + 10, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 10, 2, loop)
    elif call.data == 'show_pp_4':
        text = f"Пункт {int(number) + 10}.1\n"+str(await search.main_to_text(int(number) + 10, 2))
        await UsersDbManager.update_pp(tel_id, int(number)+ 10, 2, loop)
    elif call.data == 'show_pp_5':
        text = f"Пункт {int(number) + 10}.1\n"+str(await search.main_to_text(int(number) + 10, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 10, 2, loop)
    elif call.data == 'show_pp_6':
        text = f"Пункт {int(number) + 10}.1\n"+ str(await search.main_to_text(int(number) + 10, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 10, 2, loop)
    elif call.data == 'show_pp_7':
        text = f"Пункт {int(number) + 10}.1\n"+str(await search.main_to_text(int(number) + 10, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 10, 2, loop)
    elif call.data == 'show_pp_8':
        text = f"Пункт {int(number) + 10}.1\n"+str(await search.main_to_text(int(number) + 10, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 10, 2, loop)
    elif call.data == 'show_pp_9':
        text =f"Пункт {int(number) + 10}.1\n"+str(await search.main_to_text(int(number) + 10, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 10, 2, loop)
    await bot.send_message(tel_id, text, reply_markup=keyboard)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(lambda call:
                           call.data.startswith('show_ppp_0') or
                           call.data.startswith('show_ppp_1') or
                           call.data.startswith('show_ppp_2') or
                           call.data.startswith('show_ppp_3') or
                           call.data.startswith('show_ppp_4') or
                           call.data.startswith('show_ppp_5') or
                           call.data.startswith('show_ppp_6') or
                           call.data.startswith('show_ppp_7') or
                           call.data.startswith('show_ppp_8') or
                           call.data.startswith('show_ppp_9'))
async def _back(call):
    tel_id = call.message.chat.id
    keyboard = mk.next_back()
    number = call.data[9:]
    text = ''
    if call.data == 'show_ppp_0':
        text = f"Пункт {int(number) + 20}.1\n"+str(await search.main_to_text(int(number) + 20, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 20, 2, loop)
    elif call.data == 'show_ppp_1':
        text = f"Пункт {int(number) + 20}.1\n"+str(await search.main_to_text(int(number) + 20, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 20, 2, loop)
    elif call.data == 'show_ppp_2':
        text = f"Пункт {int(number) + 20}.1\n"+str(await search.main_to_text(int(number) + 20, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 20, 2, loop)
    elif call.data == 'show_ppp_3':
        text = f"Пункт {int(number) + 20}.1\n"+str(await search.main_to_text(int(number) + 20, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 20, 2, loop)
    elif call.data == 'show_ppp_4':
        text = f"Пункт {int(number) + 20}.1\n"+str(await search.main_to_text(int(number) + 20, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 20, 2, loop)
    elif call.data == 'show_ppp_5':
        text = f"Пункт {int(number) + 20}.1\n"+str(await search.main_to_text(int(number) + 20, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 20, 2, loop)
    elif call.data == 'show_ppp_6':
        text = f"Пункт {int(number) + 20}.1\n"+str(await search.main_to_text(int(number) + 20, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 20, 2, loop)
    elif call.data == 'show_ppp_7':
        text = f"Пункт {int(number) + 20}.1\n"+str(await search.main_to_text(int(number) + 20, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 20, 2, loop)
    elif call.data == 'show_ppp_8':
        text = f"Пункт {int(number) + 20}.1\n"+str(await search.main_to_text(int(number) + 20, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 20, 2, loop)
    elif call.data == 'show_ppp_9':
        text = f"Пункт {int(number) + 20}.1\n"+str(await search.main_to_text(int(number) + 20, 1))
        await UsersDbManager.update_pp(tel_id, int(number)+ 20, 2, loop)
    await bot.send_message(tel_id, text, reply_markup=keyboard)
    await bot.delete_message(call.message.chat.id, call.message.message_id)



@dp.callback_query_handler(lambda call:
                           call.data.startswith('show_pppp_0') or
                           call.data.startswith('show_pppp_1') or
                           call.data.startswith('show_pppp_2'))
async def _back(call):
    tel_id = call.message.chat.id
    keyboard = mk.next_back()
    number = call.data[10:]
    text = ''
    if call.data == 'show_pppp_0':
        text = f"Пункт {int(number) + 30}.1\n"+str(await search.main_to_text(int(number) + 30, 1))
        await UsersDbManager.update_pp(tel_id, int(number) + 30, 2, loop)
    elif call.data == 'show_pppp_1':
        text = f"Пункт {int(number) + 30}.1\n"+str(await search.main_to_text(int(number) + 30, 1))
        await UsersDbManager.update_pp(tel_id, int(number) + 30, 2, loop)
    elif call.data == 'show_pppp_2':
        text = f"Пункт {int(number) + 30}.1\n"+str(await search.main_to_text(int(number) + 30, 1))
        await UsersDbManager.update_pp(tel_id, int(number) + 30, 2, loop)
    await bot.send_message(tel_id, text, reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data.startswith('show_next'))
async def wer(call):
    tel_id = call.message.chat.id
    if await UsersDbManager.get_context(tel_id, loop) == 'minus':
        await UsersDbManager.update_context(tel_id, '', loop)
        nums = await UsersDbManager.get_pp(tel_id, loop)
        num = nums[1]
        await UsersDbManager.update_pp(tel_id, nums[0], num+1, loop)
        nums = await UsersDbManager.get_pp(tel_id, loop)
        num = nums[1]
        num += 1
        if num == 2:
            text = f"Пункт {nums[0]}.{num}\n" + str(await search.main_to_text(nums[0], 2))
            keyboard = mk.next_back()
            await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
            await UsersDbManager.update_pp(tel_id, nums[0], num, loop)
        else:
            await UsersDbManager.update_pp(tel_id, nums[0], num, loop)
            num = nums[1]
            w = await search.get_count(nums[0])
            if num <= w:
                if nums[0] ==1 and num ==10:
                    text=f"Пункт {nums[0]}.{num}\n"+'Термины ПДД:\nhttps://telegra.ph/Terminy-privedennye-v-ehtih-Pravilah-imeyut-sleduyushchee-znachenie-11-27'
                    keyboard = mk.next_back()
                    await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
                else:
                    text = f"Пункт {nums[0]}.{num}\n"+str(await search.main_to_text(nums[0], num))
                    keyboard = mk.next_back()
                    await bot.edit_message_text(text,tel_id, call.message.message_id, reply_markup=keyboard)
            elif num > w:
                await bot.edit_message_text('Вы прочитали все пункты в этом разделе. Переходите к следующим разделам!', tel_id,
                                            call.message.message_id, reply_markup=mk.show_pdd_cat())
    else:
        nums = await UsersDbManager.get_pp(tel_id, loop)
        num = nums[1]
        num += 1
        if num == 2:
            await UsersDbManager.update_pp(tel_id, nums[0], num, loop)
            text = f"Пункт {nums[0]}.{num}\n" + str(await search.main_to_text(nums[0], 2))
            keyboard = mk.next_back()
            await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
        else:
            await UsersDbManager.update_pp(tel_id, nums[0], num, loop)
            num = nums[1]
            w = await search.get_count(nums[0])
            if num <= w:
                if nums[0] == 1 and num == 10:
                    text = f"Пункт {nums[0]}.{num}\n" + 'Термины ПДД:\nhttps://telegra.ph/Terminy-privedennye-v-ehtih-Pravilah-imeyut-sleduyushchee-znachenie-11-27'
                    keyboard = mk.next_back()
                    await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
                else:
                    text = f"Пункт {nums[0]}.{num}\n" + str(await search.main_to_text(nums[0], num))
                    keyboard = mk.next_back()
                    await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
            elif num > w:
                await bot.edit_message_text('Вы прочитали все пункты в этом разделе. Переходите к следующим разделам!',
                                            tel_id,
                                            call.message.message_id, reply_markup=mk.show_pdd_cat())


@dp.callback_query_handler(lambda call: call.data.startswith('show_pred'))
async def wer(call):
    tel_id = call.message.chat.id
    nums = await UsersDbManager.get_pp(tel_id, loop)
    num = nums[1]
    if await UsersDbManager.get_context(tel_id, loop) == '':
        await UsersDbManager.update_context(tel_id, 'minus', loop)
        await UsersDbManager.update_pp(tel_id, nums[0], num-1, loop)
        nums = await UsersDbManager.get_pp(tel_id, loop)
        num = nums[1]
        num -=1
        if num > 1:
            text = f"Пункт {nums[0]}.{num}\n" + str(await search.main_to_text(nums[0], num))
            keyboard = mk.next_back()
            await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
            await UsersDbManager.update_pp(tel_id, nums[0], num, loop)
        elif num == 1:

            text = f"Пункт {nums[0]}.{num}\n" + str(await search.main_to_text(nums[0], 1))
            keyboard = mk.next_back()
            await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
            await UsersDbManager.update_pp(tel_id, nums[0], num, loop)
        elif num == 0:
            await bot.edit_message_text('Переходите к следующим разделам!', tel_id,
                                        call.message.message_id, reply_markup=mk.show_pdd_cat())
    elif await UsersDbManager.get_context(tel_id, loop) == 'minus':
        nums = await UsersDbManager.get_pp(tel_id, loop)
        num = nums[1]
        num -= 1
        if num >1:
            text = f"Пункт {nums[0]}.{num}\n" + str(await search.main_to_text(nums[0], num))
            keyboard = mk.next_back()
            await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
            await UsersDbManager.update_pp(tel_id, nums[0], num, loop)
        elif num == 1:

            text = f"Пункт {nums[0]}.{num}\n" + str(await search.main_to_text(nums[0], 1))
            keyboard = mk.next_back()
            await bot.edit_message_text(text, tel_id, call.message.message_id, reply_markup=keyboard)
            await UsersDbManager.update_pp(tel_id, nums[0], num, loop)
        elif num == 0:
            await bot.edit_message_text('Переходите к следующим разделам!', tel_id,
                                        call.message.message_id, reply_markup=mk.show_pdd_cat())


@dp.inline_handler(lambda inline_query: inline_query.query.startswith('show_zn_'))
async def show_zn_inl(inline_query):
    print(900909)
    article = inline_query.query[5:]
    tel_id = inline_query.from_user.id
    user = await UsersDbManager.get_user(tel_id, loop)
    products = await UsersDbManager.get_sign(article, loop)

    if len(products) == 0:
        text = 'Произошла ошибка, попробуйте позже'

        result_id = str(uuid.uuid4())
        message_content = InputTextMessageContent(text)
        result = InlineQueryResultArticle(
            id=result_id, title=text,
            thumb_url='https://img.icons8.com/dotty/2x/nothing-found.png',
            thumb_height=400, thumb_width=400,
            input_message_content=message_content
        )
        await bot.answer_inline_query(inline_query.id, results=[result], cache_time=1)
        return

    if inline_query.offset != '':
        offset = int(inline_query.offset)
    else:
        offset = 0

    if len(products) < offset + 3:
        next_offset = ''
        end = len(products)
    else:
        next_offset = offset + 3
        end = next_offset

    results = []
    for i in range(offset, end):
        product = products[i]

        try:
            category = product[0]
            name = product[1]
            image_url = f'https://vodiy.ua/media/trafficsign_image/{str(product[4])}.png'

            result_id = str(uuid.uuid4())

            item_description = await search.get_item_description(product, loop)
            message_content = InputTextMessageContent(item_description, parse_mode='html')
        except KeyError:
            continue

        results.append(
            InlineQueryResultArticle(
                id=result_id, title=name,
                thumb_url=image_url,
                thumb_height=400, thumb_width=400,
                input_message_content=message_content,
            ))

    try:
        await bot.answer_inline_query(inline_query.id, results=results, next_offset=str(next_offset), cache_time=1)
    except aiogram.utils.exceptions.NetworkError:
        print('Network error, file too large')


@dp.inline_handler(lambda inline_query: inline_query.query.startswith('razm_'))
async def show_zn_inl(inline_query):
    article = inline_query.query[5:]
    tel_id = inline_query.from_user.id
    user = await UsersDbManager.get_user(tel_id, loop)
    products = await UsersDbManager.get_sign_2(article, loop)

    if len(products) == 0:
        text = 'Произошла ошибка, попробуйте позже'

        result_id = str(uuid.uuid4())
        message_content = InputTextMessageContent(text)
        result = InlineQueryResultArticle(
            id=result_id, title=text,
            thumb_url='https://img.icons8.com/dotty/2x/nothing-found.png',
            thumb_height=400, thumb_width=400,
            input_message_content=message_content
        )
        await bot.answer_inline_query(inline_query.id, results=[result], cache_time=1)
        return

    if inline_query.offset != '':
        offset = int(inline_query.offset)
    else:
        offset = 0

    if len(products) < offset + 3:
        next_offset = ''
        end = len(products)
    else:
        next_offset = offset + 3
        end = next_offset

    results = []
    links = {"2.1": '_3', "2.2": '_2', "2.3": '_2', "2.4": '_3', "2.5": '_2', "2.6": '', "2.7": ''}
    for i in range(offset, end):
        product = products[i]
        if article == "Вертикальная":
            try:
                category = product[0]
                name = product[1]
                image_url = None
                image_url = f'https://vodiy.ua/media/trafficsign_image/{str(product[4])}.r{str(links.get(product[4]))}.png'
                print(image_url)
                result_id = str(uuid.uuid4())

                item_description = await search.get_description(product, loop)
                message_content = InputTextMessageContent(item_description, parse_mode='html')
            except KeyError:
                continue

            results.append(
                InlineQueryResultArticle(
                    id=result_id, title=name,
                    thumb_url=image_url,
                    thumb_height=400, thumb_width=400,
                    input_message_content=message_content,
                ))

        else:
            try:
                category = product[0]
                name = product[1]
                image_url = None
                image_url = f'https://vodiy.ua/media/trafficsign_image/{str(product[4])}r.png'
                print(image_url)
                result_id = str(uuid.uuid4())

                item_description = await search.get_description(product, loop)
                message_content = InputTextMessageContent(item_description, parse_mode='html')
            except KeyError:
                continue

            results.append(
                InlineQueryResultArticle(
                    id=result_id, title=name,
                    thumb_url=image_url,
                    thumb_height=400, thumb_width=400,
                    input_message_content=message_content,
                ))

    try:
        await bot.answer_inline_query(inline_query.id, results=results, next_offset=str(next_offset), cache_time=1)
    except:
        print('Network error, file too large')

'''
Для администратора
'''

'''
_____________________________________________________________admin commands_____________________________________________
'''
@dp.message_handler(lambda message:
                    message.text == 'admin'
                    or message.text =='Admin')
async def admin(message):
    tel_id = message.chat.id
    text = f'Добрейшего времени суток.\nВведите пароль:'
    await UsersDbManager.update_context(tel_id, 'get_password', loop)
    await bot.send_message(tel_id, text, disable_notification=True)

@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context(message.chat.id) == 'get_password')
async def set_zn_text(message):
    tel_id = message.chat.id
    await UsersDbManager.update_context(tel_id, '0', loop)
    if str(message.text) == config.__AdminPassword__:
        text = 'Добро пожаловать!'
        keyboard = mk.get_admin_keyboard()
        await UsersDbManager.update_context(tel_id, '', loop)
    else:
        text = 'Неправильный пароль!'
        keyboard = mk.main_menu_ru
        username = message.from_user.username
        tt = f'Кто-то пытался войти в запись администратора\nTelegram id: {tel_id}\nНик: @{username}\nДата, время: {datetime.datetime.now().date()} {datetime.datetime.now().time()}'
        await bot.send_message(config.Owner_id, tt)
    await bot.send_message(tel_id, text, reply_markup=keyboard, disable_notification=True)

@dp.callback_query_handler(lambda call:
                           call.data.startswith('stat'))
async def stat(call):
    tel_id = call.message.chat.id
    count, count_new, count_t, count_r, count_e, sr = await UsersDbManager.for_stat(loop)
    text = f'Всего пользователей : {count}\n' \
           f'Новые пользователи за последний месяц : {count_new}\n' \
           f'Количество пройденых тестов : {count_t}\n' \
           f'Количество удачно пройденых тестов : {count_r}\n' \
           f'Количество неудачно пройденых тестов : {count_e}\n' \
           f'Среднее количество тестов пройденых пользователем : {sr}\n'
    keyboard = mk.get_admin_keyboard()
    await bot.send_message(tel_id, text, disable_notification= True, reply_markup=keyboard)

@dp.callback_query_handler(lambda call:
                           call.data.startswith('rass'))
async def rass(call):
    tel_id = call.message.chat.id
    await UsersDbManager.update_context(tel_id, 'wtr', loop)
    await bot.send_message(tel_id, "Ожидаю то, что нужно разослать пользователям...", reply_markup=mk.back_admin())

@dp.message_handler(lambda message:
                    UsersDbManager.sync_get_context(message.chat.id) == 'wtr')
async def text_ras(message):
    tel_id = message.chat.id
    await UsersDbManager.update_context(tel_id, '', loop)
    message_id = message.message_id
    message_text = "!!! Рассылка !!!\n" + message.text
    users = await UsersDbManager.all_users(loop)
    for user in users[0]:
        await bot.send_message(user, message_text)
    await bot.send_message(tel_id, "Рассылка прошла успешно", reply_markup=mk.get_admin_keyboard())


@dp.callback_query_handler(lambda call:
                           call.data.startswith('Cancel_ad'))
async def rass(call):
    tel_id = call.message.chat.id
    await bot.send_message(tel_id, "Меню администратора", reply_markup=mk.get_admin_keyboard())


'''
Распознавание знаков
'''

@dp.message_handler(lambda message:
                    message.text == 'Распознать знак')
async def sss(message):
    tel_id = message.chat.id
    await bot.send_message(tel_id, 'Для более точного распознания отправьте фото знака крупныи планом.', disable_notification=True)
    await bot.send_photo(tel_id, 'https://juristpomog.com/wp-content/uploads/2018/05/2013-03-04-dorznak-300x200.jpg',
                         'Пример фотографии знака', disable_notification=True)
    await UsersDbManager.update_context(tel_id, 'wait_sign_photo', loop)
    print(UsersDbManager.sync_get_context(message.chat.id))

@dp.message_handler(content_types=tp.ContentType.ANY)
async def sss1(message):
    tel_id = message.chat.id
    photo = None
    context = await UsersDbManager.get_context(tel_id, loop)
    items = None
    if context == 'wait_sign_photo':
        await UsersDbManager.update_context(tel_id, '', loop)
        photo = message.photo[-1].file_id
        file_info = await bot.get_file(photo)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        sign = dt.classify(BytesIO(file.content))
        items = await UsersDbManager.get_sign_for_detection(sign, loop)
        try:
            text = await search.get_item_description(items[0], loop)
            print(text)
            await bot.send_message(tel_id, text, disable_notification=True, parse_mode='html')
        except:
            await bot.send_message(tel_id, 'К сожалению произошла ошибка. Попробуйте немного позже', disable_notification=True)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
