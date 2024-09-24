from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from . import database as db

to_main_menu = InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')
to_menu_only = InlineKeyboardMarkup(inline_keyboard=[[to_main_menu]])

catalog = InlineKeyboardButton(text='🛍️ Каталог', callback_data='to_catalog')
profile = InlineKeyboardButton(text='👤 Профиль', callback_data='profile')
comments = InlineKeyboardButton(text='🌟 Отзывы', url='https://plati.market/seller/misterheisenberg/1083350/')

def create_main_menu():
    builder = InlineKeyboardBuilder()

    builder.row(catalog)
    builder.row(profile)
    builder.row(comments)
    return builder.as_markup()

main_menu = create_main_menu()

def create_catalog(categories, path):
    builder = InlineKeyboardBuilder()
    for category in categories:
        if path=='':
            callback=f'catalog{path}_{category}'
        elif path=='product':
            callback=f'product_{category}'
        else:
            callback=f'catalog_{path}_{category}'
        builder.row(InlineKeyboardButton(text=category, callback_data=callback))
    builder.row(catalog)
    builder.row(to_main_menu)
    return builder.as_markup()


buy = InlineKeyboardButton(text='✅ Купить', callback_data='buy')
product_menu = InlineKeyboardMarkup(inline_keyboard=[[buy], [catalog], [to_main_menu]])

count = InlineKeyboardButton(text='Ввести количество', callback_data='count')
counted_menu = InlineKeyboardMarkup(inline_keyboard=[[count], [catalog], [to_main_menu]])

topup = InlineKeyboardButton(text='💵 Пополнить', callback_data='topup')
topup_menu = InlineKeyboardMarkup(inline_keyboard=[[topup], [catalog]])

apply_buy = InlineKeyboardButton(text='✅ Подтвердить', callback_data='apply_buy')
apply_transactions = InlineKeyboardMarkup(inline_keyboard=[[apply_buy], [catalog]])

sales = InlineKeyboardButton(text='Все покупки', callback_data='all_sales')
activate_code = InlineKeyboardButton(text='Активировать код', callback_data='code')
profile_menu = InlineKeyboardMarkup(inline_keyboard=[[sales], [topup], [to_main_menu]])

def get_topup_methods():
    methods = db.get_topup_methods()
    builder = InlineKeyboardBuilder()
    for method in methods:
        builder.row(InlineKeyboardButton(text=method.name, callback_data=method.callback))
    builder.row(to_main_menu)
    return builder.as_markup()

topup_methods = get_topup_methods()
