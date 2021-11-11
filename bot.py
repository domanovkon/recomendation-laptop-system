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


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
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
    elif call.data == "lap_filter":
        bot.send_message(call.message.chat.id, 'Выбери тип ноутбука')


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    keyboard = types.InlineKeyboardMarkup()
    key_list = types.InlineKeyboardButton(text='Показать список товаров на складе', callback_data="lap_list")
    keyboard.add(key_list)
    key_filt = types.InlineKeyboardButton(text='Подобрать ноутбук по параметрам', callback_data="lap_filter")
    keyboard.add(key_filt)
    bot.send_message(message.from_user.id, "Я тебя не понимаю", reply_markup=keyboard)


bot.polling()
