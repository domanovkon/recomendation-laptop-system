import numpy as np
import telebot
import pymorphy2
import pandas as pd
from token_api import TOKEN_API
from telebot import types, util
from smiles import sml

bot = telebot.TeleBot(TOKEN_API)


@bot.message_handler(commands=['start'])
def command_help(message):
    photo = open('svidetel.png', 'rb')
    bot.send_photo(message.from_user.id, photo)
    keyboard = types.InlineKeyboardMarkup()
    key_list = types.InlineKeyboardButton(text='Показать список всех товаров на складе', callback_data="lap_list")
    keyboard.add(key_list)
    key_filt = types.InlineKeyboardButton(text='Подобрать ноутбук по параметрам', callback_data="lap_filter")
    keyboard.add(key_filt)
    bot.send_message(message.from_user.id, "Привет 👋👋👋 \n выбери что хочешь сделать 🤔", reply_markup=keyboard)


dataSetSearch123 = pd.read_csv('laptops.txt', delimiter='\t', encoding="utf-16-le",
                               usecols=['Тип видеокарты', 'Цена', 'Категория', 'Количество_ОЗУ', 'Процессор',
                                        'Ноутбук'])

laptopTree = [["Встроенная", "Дискретная"],
              ["Высокая", "Низкая"],
              ["Ноутбуки", "Ультрабуки", "Геймерские"],
              [4, 8, 16, 32],
              ["AMD", "Intel"]]

weights = [0.4, 0.3, 0.2, 0.3, 0.1]


def diff_tree(t1, t2):
    difftree = []
    for i in range(0, 5):
        difftree.append(abs(laptopTree[i].index(t1[i]) - laptopTree[i].index(t2[i])))
    similarity = 0
    for i in range(len(difftree)):
        similarity += difftree[i] * weights[i]
    return similarity


def searchSimulariry():
    dfSearch = pd.DataFrame({'Тип видеокарты': [gpu_type.title()],
                             'Цена': [prices_category.title()],
                             'Категория': [laptop_type.title()],
                             'Количество_ОЗУ': ram_amount,
                             'Процессор': cpu_type})

    func = diff_tree
    dataset = dataSetSearch123
    return (getSimilarsInSearch(dataset, dataSetSearch123, func, dfSearch).sort_values("Величина различия"))


def getSimilarsInSearch(ds, dataSet, metric, dfSearch):
    r = []
    for i in range(len(ds.values.tolist())):
        r.append(metric(dfSearch.values.tolist()[0], ds.values.tolist()[i]))

    return pd.DataFrame(list(zip(r, map(lambda e: str("   ".join(e[-1:])),
                                        dataSet.values.tolist()))), index=np.arange(len(r)),
                        columns=['Величина различия', 'Ноут'])


def get_likes(message):
    print(message.text)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global gpu_type
    global prices_category
    global laptop_type
    global ram_amount
    global cpu_type
    if call.data == "lap_list":
        dataSetSearch = pd.read_csv('laptops.txt', delimiter='\t', encoding="utf-16-le",
                                    usecols=['Тип видеокарты', 'Цена', 'Категория', 'Количество_ОЗУ', 'Процессор',
                                             'Ноутбук'])
        columns_titles = ["Ноутбук", 'Категория', 'Процессор', 'Количество_ОЗУ', "Тип видеокарты", 'Цена']
        dataSetSearch = dataSetSearch.reindex(columns=columns_titles)

        laptop_list_counter = 0
        for x in dataSetSearch.values.tolist():
            laptop_list_counter = laptop_list_counter + 1
            str1 = x[0] + "\n" + "Категория: " + x[1] + "\n" + "Процессор: " + x[2] + "\n" + \
                   "Количество ОЗУ: " + str(x[3]) + "\n" + "Тип видеокарты: " + x[4] + "\n" + "Цена: " + x[5]
            bot.send_message(call.message.chat.id, sml[laptop_list_counter] + " " + str1 + " 😎")
        keyboard = types.InlineKeyboardMarkup()
        key_list = types.InlineKeyboardButton(text='Показать список всех товаров на складе', callback_data="lap_list")
        keyboard.add(key_list)
        key_filt = types.InlineKeyboardButton(text='Подобрать ноутбук по параметрам', callback_data="lap_filter")
        keyboard.add(key_filt)
        key_like = types.InlineKeyboardButton(text='Показать похожие', callback_data="lap_like")
        keyboard.add(key_like)
        bot.send_message(call.message.chat.id, "Выбери что хочешь сделать дальше🤔", reply_markup=keyboard)
    elif call.data == "lap_like":
        bot.send_message(call.message.chat.id, "Введи номера понравившихся ноутбуков через пробел 👍🏻")
        bot.register_next_step_handler(call.message, get_likes)
    elif call.data == "lap_filter" or call.data == "filt_no":
        keyboard = types.InlineKeyboardMarkup()
        gpu_disk_k = types.InlineKeyboardButton(text='Дискретная', callback_data="disk")
        keyboard.add(gpu_disk_k)
        gpu_inside_k = types.InlineKeyboardButton(text='Встроенная', callback_data="inside")
        keyboard.add(gpu_inside_k)
        if call.data == "lap_filter":
            bot.send_message(call.message.chat.id, 'Подбор ноутбука по параметрам 🤓')
        elif call.data == "filt_no":
            bot.send_message(call.message.chat.id, 'Попробуем еще раз 🤓')
        bot.send_message(call.message.chat.id, 'Выберите тип видеокарты 🌈', reply_markup=keyboard)
    elif call.data == "disk":
        gpu_type = "Дискретная"
        keyboard = types.InlineKeyboardMarkup()
        price_h = types.InlineKeyboardButton(text='Высокая', callback_data="high")
        keyboard.add(price_h)
        price_l = types.InlineKeyboardButton(text='Низкая', callback_data="low")
        keyboard.add(price_l)
        bot.send_message(call.message.chat.id, 'Выберите ценовую категорию 💲', reply_markup=keyboard)
    elif call.data == "inside":
        gpu_type = "Встроенная"
        keyboard = types.InlineKeyboardMarkup()
        price_h = types.InlineKeyboardButton(text='Высокая', callback_data="high")
        keyboard.add(price_h)
        price_l = types.InlineKeyboardButton(text='Низкая', callback_data="low")
        keyboard.add(price_l)
        bot.send_message(call.message.chat.id, 'Выберите ценовую категорию 💲', reply_markup=keyboard)
    elif call.data == "high":
        prices_category = "Высокая"
        keyboard = types.InlineKeyboardMarkup()
        lap = types.InlineKeyboardButton(text='Ноутбуки', callback_data="lap")
        keyboard.add(lap)
        ult = types.InlineKeyboardButton(text='Ультрабуки', callback_data="ult")
        keyboard.add(ult)
        game = types.InlineKeyboardButton(text='Геймерские', callback_data="game")
        keyboard.add(game)
        bot.send_message(call.message.chat.id, 'Выберите тип ноутбука 🙃', reply_markup=keyboard)
    elif call.data == "low":
        prices_category = "Низкая"
        keyboard = types.InlineKeyboardMarkup()
        lap = types.InlineKeyboardButton(text='Ноутбуки', callback_data="lap")
        keyboard.add(lap)
        ult = types.InlineKeyboardButton(text='Ультрабуки', callback_data="ult")
        keyboard.add(ult)
        game = types.InlineKeyboardButton(text='Геймерские ноутбуки', callback_data="game")
        keyboard.add(game)
        bot.send_message(call.message.chat.id, 'Выберите тип ноутбука 🙃', reply_markup=keyboard)
    elif call.data == "lap":
        laptop_type = "Ноутбуки"
        keyboard = types.InlineKeyboardMarkup()
        ram4 = types.InlineKeyboardButton(text='4', callback_data="ram4")
        keyboard.add(ram4)
        ram8 = types.InlineKeyboardButton(text='8', callback_data="ram8")
        keyboard.add(ram8)
        ram16 = types.InlineKeyboardButton(text='16', callback_data="ram16")
        keyboard.add(ram16)
        ram32 = types.InlineKeyboardButton(text='32', callback_data="ram32")
        keyboard.add(ram32)
        bot.send_message(call.message.chat.id, 'Сколько оперативы нужно ⛰', reply_markup=keyboard)
    elif call.data == "ult":
        laptop_type = "Ультрабуки"
        keyboard = types.InlineKeyboardMarkup()
        ram4 = types.InlineKeyboardButton(text='4', callback_data="ram4")
        keyboard.add(ram4)
        ram8 = types.InlineKeyboardButton(text='8', callback_data="ram8")
        keyboard.add(ram8)
        ram16 = types.InlineKeyboardButton(text='16', callback_data="ram16")
        keyboard.add(ram16)
        ram32 = types.InlineKeyboardButton(text='32', callback_data="ram32")
        keyboard.add(ram32)
        bot.send_message(call.message.chat.id, 'Сколько оперативы нужно ⛰', reply_markup=keyboard)
    elif call.data == "game":
        laptop_type = "Геймерские"
        keyboard = types.InlineKeyboardMarkup()
        ram4 = types.InlineKeyboardButton(text='4', callback_data="ram4")
        keyboard.add(ram4)
        ram8 = types.InlineKeyboardButton(text='8', callback_data="ram8")
        keyboard.add(ram8)
        ram16 = types.InlineKeyboardButton(text='16', callback_data="ram16")
        keyboard.add(ram16)
        ram32 = types.InlineKeyboardButton(text='32', callback_data="ram32")
        keyboard.add(ram32)
        bot.send_message(call.message.chat.id, 'Сколько оперативы нужно ⛰', reply_markup=keyboard)
    elif call.data == "ram4":
        ram_amount = 4
        keyboard = types.InlineKeyboardMarkup()
        amd = types.InlineKeyboardButton(text='AMD', callback_data="amd")
        keyboard.add(amd)
        intel = types.InlineKeyboardButton(text='Intel', callback_data="intel")
        keyboard.add(intel)
        bot.send_message(call.message.chat.id, 'Производитель процессора 🔨', reply_markup=keyboard)
    elif call.data == "ram8":
        ram_amount = 8
        keyboard = types.InlineKeyboardMarkup()
        amd = types.InlineKeyboardButton(text='AMD', callback_data="amd")
        keyboard.add(amd)
        intel = types.InlineKeyboardButton(text='Intel', callback_data="intel")
        keyboard.add(intel)
        bot.send_message(call.message.chat.id, 'Производитель процессора 🔨', reply_markup=keyboard)
    elif call.data == "ram16":
        ram_amount = 16
        keyboard = types.InlineKeyboardMarkup()
        amd = types.InlineKeyboardButton(text='AMD', callback_data="amd")
        keyboard.add(amd)
        intel = types.InlineKeyboardButton(text='Intel', callback_data="intel")
        keyboard.add(intel)
        bot.send_message(call.message.chat.id, 'Производитель процессора 🔨', reply_markup=keyboard)
    elif call.data == "ram32":
        ram_amount = 32
        keyboard = types.InlineKeyboardMarkup()
        amd = types.InlineKeyboardButton(text='AMD', callback_data="amd")
        keyboard.add(amd)
        intel = types.InlineKeyboardButton(text='Intel', callback_data="intel")
        keyboard.add(intel)
        bot.send_message(call.message.chat.id, 'Процессор от 🔨', reply_markup=keyboard)
    elif call.data == "amd":
        cpu_type = "AMD"
        keyboard = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton(text='Да', callback_data="filt_yes")
        keyboard.add(yes)
        no = types.InlineKeyboardButton(text='Нет', callback_data="filt_no")
        keyboard.add(no)
        bot.send_message(call.message.chat.id,
                         'Вы выбрали:\nТип видеокарты 🌈 ' + gpu_type + '\nЦена 💲 ' + prices_category
                         + '\nКатегория 🙃 ' + laptop_type + '\nКоличество оперативы ⛰ ' + str(
                             ram_amount) + '\nПроцессор 🔨 '
                         + cpu_type + '\nВсе верно ❓', reply_markup=keyboard)
    elif call.data == "intel":
        cpu_type = "Intel"
        keyboard = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton(text='Да', callback_data="filt_yes")
        keyboard.add(yes)
        no = types.InlineKeyboardButton(text='Нет', callback_data="filt_no")
        keyboard.add(no)
        bot.send_message(call.message.chat.id,
                         'Вы выбрали:\nТип видеокарты 🌈 ' + gpu_type + '\nЦена 💲 ' + prices_category
                         + '\nКатегория 🙃 ' + laptop_type + '\nКоличество оперативы ⛰ ' + str(
                             ram_amount) + '\nПроцессор 🔨 '
                         + cpu_type + '\nВсе верно ❓', reply_markup=keyboard)
    elif call.data == "filt_yes":
        dataSetSearch = pd.read_csv('laptops.txt', delimiter='\t', encoding="utf-16-le",
                                    usecols=['Тип видеокарты', 'Цена', 'Категория', 'Количество_ОЗУ', 'Процессор',
                                             'Ноутбук'])
        gpu_search = dataSetSearch[dataSetSearch["Тип видеокарты"] == gpu_type.title()]
        prices_search = gpu_search[gpu_search["Цена"] == prices_category.title()]
        laptop_type_search = prices_search[prices_search["Категория"] == laptop_type.title()]
        ram_amounts_search = laptop_type_search[laptop_type_search["Количество_ОЗУ"] == ram_amount]
        cpu_search = ram_amounts_search[ram_amounts_search["Процессор"] == cpu_type]
        if cpu_search.empty:
            bot.send_message(call.message.chat.id,
                             "В наличии нет ноутбуков с такими параметрами 😥\nВозможно вас заинтересуют похожие")
            lap_array = searchSimulariry().values.tolist()
            laptop_list_counter = 0
            for x in lap_array:
                if laptop_list_counter == 5:
                    break
                laptop_list_counter = laptop_list_counter + 1
                str1 = x[1] + '\n'
                bot.send_message(call.message.chat.id, sml[laptop_list_counter] + " " + str1)
            keyboard = types.InlineKeyboardMarkup()
            key_list = types.InlineKeyboardButton(text='Показать список всех товаров на складе',
                                                  callback_data="lap_list")
            keyboard.add(key_list)
            key_filt = types.InlineKeyboardButton(text='Подобрать ноутбук по параметрам', callback_data="lap_filter")
            keyboard.add(key_filt)
            bot.send_message(call.message.chat.id, "Выбери что хочешь сделать дальше🤔", reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, "Результаты поиска")
            columns_titles = ["Ноутбук", 'Категория', 'Процессор', 'Количество_ОЗУ', "Тип видеокарты", 'Цена']
            dataSetSearch = cpu_search.reindex(columns=columns_titles)

            laptop_list_counter = 0
            for x in dataSetSearch.values.tolist():
                laptop_list_counter = laptop_list_counter + 1
                str1 = x[0] + "\n" + "Категория: " + x[1] + "\n" + "Процессор: " + x[2] + "\n" + \
                       "Количество ОЗУ: " + str(x[3]) + "\n" + "Тип видеокарты: " + x[4] + "\n" + "Цена: " + x[5]
                bot.send_message(call.message.chat.id, sml[laptop_list_counter] + " " + str1 + " 😎")
            keyboard = types.InlineKeyboardMarkup()
            key_list = types.InlineKeyboardButton(text='Показать список всех товаров на складе',
                                                  callback_data="lap_list")
            keyboard.add(key_list)
            key_filt = types.InlineKeyboardButton(text='Подобрать ноутбук по параметрам', callback_data="lap_filter")
            keyboard.add(key_filt)
            bot.send_message(call.message.chat.id, "Выбери что хочешь сделать дальше🤔", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    keyboard = types.InlineKeyboardMarkup()
    key_list = types.InlineKeyboardButton(text='Показать список товаров на складе', callback_data="lap_list")
    keyboard.add(key_list)
    key_filt = types.InlineKeyboardButton(text='Подобрать ноутбук по параметрам', callback_data="lap_filter")
    keyboard.add(key_filt)
    bot.send_message(message.from_user.id, "Я тебя не понимаю, что ты от меня хочешь ❓", reply_markup=keyboard)


bot.polling()
