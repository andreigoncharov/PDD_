from aiogram.types import reply_keyboard, inline_keyboard
import scripts.messages as ms
import random

main_menu_ru = reply_keyboard.ReplyKeyboardMarkup([['Почитать теорию', 'Пройти тест'],
                                                   ['Мои результаты', 'Распознать знак']])


theory_category = reply_keyboard.ReplyKeyboardMarkup([[ms.theory_category[0]],
                                                        [ms.theory_category[1]],
                                                        [ms.theory_category[2]],
                                                        ['⬅️ Назад']])


tabl = reply_keyboard.ReplyKeyboardMarkup([[ms.tabl[0]],
                                                        [ms.tabl[1]],
                                                        [ms.tabl[2]],
                                                        [ms.tabl[3]],
                                                        [ms.tabl[4]],
                                                        [ms.tabl[5]],
                                                        [ms.tabl[6]],
                                                        ['⬅️ Назад']])


pdd1 = reply_keyboard.ReplyKeyboardMarkup([[ms.pdd1[0], ms.pdd1[1]],
                                          [ms.pdd1[2], ms.pdd1[3]],
                                          [ms.pdd1[4], ms.pdd1[5]],
                                          [ms.pdd1[6], ms.pdd1[7]],
                                          ['⬅️Категории', 'Страница 2 ➡️']])

pdd2 = reply_keyboard.ReplyKeyboardMarkup([[ms.pdd2[0], ms.pdd2[1]],
                                         [ms.pdd2[2], ms.pdd2[3]],
                                         [ms.pdd2[4], ms.pdd2[5]],
                                         [ms.pdd2[6], ms.pdd2[7]],
                                         ['⬅️Страница 1', 'Страница 3➡️']])

pdd3 = reply_keyboard.ReplyKeyboardMarkup([[ms.pdd3[0], ms.pdd3[1]],
                                          [ms.pdd3[2], ms.pdd3[3]],
                                          [ms.pdd3[4]], ms.pdd3[5]],
                                         [ms.pdd3[6], ms.pdd3[7]],
                                         ['⬅️Страница 2', 'Страница 4➡️'])

pdd4 = reply_keyboard.ReplyKeyboardMarkup([[ms.pdd4[0], ms.pdd4[1]],
                                          [ms.pdd4[2], ms.pdd4[3]],
                                          [ms.pdd4[4]], ms.pdd4[5]],
                                          [ms.pdd4[6], ms.pdd4[7]],
                                          ['⬅️Страница3'])

test_keyboard = reply_keyboard.ReplyKeyboardMarkup([[ms.test_keyboard[0]],
                                                     [ms.test_keyboard[1]],
                                                      ['⬅️ Назад']])

start_close = reply_keyboard.ReplyKeyboardMarkup([[ms.start_close[0]],
                                                  [ms.start_close[1]]])

start = reply_keyboard.ReplyKeyboardMarkup([[ms.start[0]],
                                                  [ms.start [1]]])

test_category = reply_keyboard.ReplyKeyboardMarkup([[ms.test_category[0]],
                                                        [ms.test_category[1]],
                                                        [ms.test_category[2]],
                                                        ['⬅️ Назад']])

def show_results_by_article(parameter):
    k = inline_keyboard.InlineKeyboardMarkup()
    text = 'Показать'

    k.add(inline_keyboard.InlineKeyboardButton(text, switch_inline_query_current_chat='show_by_article_{0}'.format(parameter)))
    return k

def next_back():
    k = inline_keyboard.InlineKeyboardMarkup()

    k.add(inline_keyboard.InlineKeyboardButton('Следующее➡️', callback_data='show_next'))
    k.add(inline_keyboard.InlineKeyboardButton('⬅️ Предыдущее', callback_data='show_pred'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[0], callback_data='to_menu'))

    return k

def yes_or_no():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Да', callback_data='cont_yes'),inline_keyboard.InlineKeyboardButton('Нет', callback_data='cont_no'))
    return k

def show_pdd_cat():
    k = inline_keyboard.InlineKeyboardMarkup()

    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd1[0], callback_data='show_p_1'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd1[1], callback_data='show_p_2'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd1[2], callback_data='show_p_3'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd1[3], callback_data='show_p_4'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd1[4], callback_data='show_p_5'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd1[5], callback_data='show_p_6'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd1[6], callback_data='show_p_7'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd1[7], callback_data='show_p_8'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[1], callback_data='to_pdd_2'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[0], callback_data='to_menu'))


    return k

def to_pdd_2():
    k = inline_keyboard.InlineKeyboardMarkup()

    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd2[0], callback_data='show_pp_9'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd2[1], callback_data='show_pp_0'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd2[2], callback_data='show_pp_1'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd2[3], callback_data='show_pp_2'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd2[4], callback_data='show_pp_3'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd2[5], callback_data='show_pp_4'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd2[6], callback_data='show_pp_5'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd2[7], callback_data='show_pp_6'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[1], callback_data='to_pdd_3'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[2], callback_data='show_pdd_cat'))

    return k

def to_pdd_3():
    k = inline_keyboard.InlineKeyboardMarkup()

    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd3[0], callback_data='show_pp_7'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd3[1], callback_data='show_pp_8'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd3[2], callback_data='show_pp_9'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd3[3], callback_data='show_ppp_0'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd3[4], callback_data='show_ppp_1'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd3[5], callback_data='show_ppp_2'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd3[6], callback_data='show_ppp_3'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd3[7], callback_data='show_ppp_4'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[1], callback_data='to_pdd_4'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[2], callback_data='to_pdd_2'))

    return k

def to_pdd_4():
    k = inline_keyboard.InlineKeyboardMarkup()

    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd4[0], callback_data='show_ppp_5'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd4[1], callback_data='show_ppp_6'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd4[2], callback_data='show_ppp_7'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd4[3], callback_data='show_ppp_8'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd4[4], callback_data='show_ppp_9'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd4[5], callback_data='show_pppp_0'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd4[6], callback_data='show_pppp_1'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.pdd4[7], callback_data='show_pppp_2'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[2], callback_data='to_pdd_3'))

    return k

def get_admin_keyboard():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Рассылка', callback_data='rass'))
    k.add(inline_keyboard.InlineKeyboardButton('Статистика', callback_data='stat'))
    return k

def back_admin():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Отмена', callback_data='Cancel_ad'))
    return k

def get_test_keyboard(count, keys_list):
    k = inline_keyboard.InlineKeyboardMarkup()
    rw_list = []
    for key in keys_list:
        if key == 1:
            rw_list.append('right')
        else:
            rw_list.append('wrong')
    print(rw_list)
    if count == 2:

        k.add(inline_keyboard.InlineKeyboardButton('A', callback_data=rw_list[0]))
        k.add(inline_keyboard.InlineKeyboardButton('B', callback_data=rw_list[1]))

    elif count == 3:
        k.add(inline_keyboard.InlineKeyboardButton('A', callback_data=rw_list[0]))
        k.add(inline_keyboard.InlineKeyboardButton('B', callback_data=rw_list[1]))
        k.add(inline_keyboard.InlineKeyboardButton('C', callback_data=rw_list[2]))

    elif count == 4:
        k.add(inline_keyboard.InlineKeyboardButton('A', callback_data=rw_list[0]))
        k.add(inline_keyboard.InlineKeyboardButton('B', callback_data=rw_list[1]))
        k.add(inline_keyboard.InlineKeyboardButton('C', callback_data=rw_list[2]))
        k.add(inline_keyboard.InlineKeyboardButton('D', callback_data=rw_list[3]))

    elif count == 5:
        k.add(inline_keyboard.InlineKeyboardButton('A', callback_data=rw_list[0]))
        k.add(inline_keyboard.InlineKeyboardButton('B', callback_data=rw_list[1]))
        k.add(inline_keyboard.InlineKeyboardButton('C', callback_data=rw_list[2]))
        k.add(inline_keyboard.InlineKeyboardButton('D', callback_data=rw_list[3]))
        k.add(inline_keyboard.InlineKeyboardButton('E', callback_data=rw_list[4]))

    #k = sorted(k, key=lambda A: random.random())
    return k

def get_cat_keyboard():
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton(ms.theory_category[0], callback_data='_cat_1'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.theory_category[1], callback_data='_cat_2'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.theory_category[2], callback_data='_cat_3'))
    return k

def show_cat():
    k = inline_keyboard.InlineKeyboardMarkup()

    k.add(inline_keyboard.InlineKeyboardButton(ms.tabl[0], switch_inline_query_current_chat='show_zn_Предупреждающие'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.tabl[1], switch_inline_query_current_chat='show_zn_Приоритета'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.tabl[2], switch_inline_query_current_chat='show_zn_Запрещающие'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.tabl[3], switch_inline_query_current_chat='show_zn_Предписывающие'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.tabl[4], switch_inline_query_current_chat='show_zn_Инф-Указ'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.tabl[5], switch_inline_query_current_chat='show_zn_Сервис'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.tabl[6], switch_inline_query_current_chat='show_zn_Таблички'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[0], callback_data='to_menu'))

    return k

def show_cat_razm():
    k = inline_keyboard.InlineKeyboardMarkup()

    k.add(inline_keyboard.InlineKeyboardButton('Горизонтальная', switch_inline_query_current_chat='razm_Горизонтальная'))
    k.add(inline_keyboard.InlineKeyboardButton('Вертикальная', switch_inline_query_current_chat='razm_Вертикальная'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[0], callback_data='to_menu'))

    return k

def cat_tabl():
    k = inline_keyboard.InlineKeyboardMarkup()

    k.add(inline_keyboard.InlineKeyboardButton(ms.razm[0], callback_data='tabl_1'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.razm[1], callback_data='tabl_2'))
    k.add(inline_keyboard.InlineKeyboardButton(ms.back_next[0], callback_data='to_menu'))

    return k