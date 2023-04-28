from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

to_menu = InlineKeyboardButton('🏠 Главное меню', callback_data='main_menu')
to_menu_only = InlineKeyboardMarkup(row_width=1).add(to_menu)


# -- Главное меню --

catalog_btn = InlineKeyboardButton('🛍 Каталог', callback_data='catalog')
balance_btn = InlineKeyboardButton('💳 Баланс', callback_data='balance')
comment_btn = InlineKeyboardButton('🗣 Отзывы', callback_data='comment')
main_menu = InlineKeyboardMarkup(row_width=1).add(catalog_btn, balance_btn, comment_btn)


# -- Баланс --

balance_deposit = InlineKeyboardButton('🪙 Пополнить', callback_data='deposit')
balance_menu = InlineKeyboardMarkup(row_width=1).add(balance_deposit, to_menu)

# -- Отзывы --

check_comments = InlineKeyboardButton('👀 Посмотреть отзывы', callback_data = 'check_comments')
add_comment = InlineKeyboardButton('✍️ Оставить отзыв', callback_data='add_comment')
comment_menu = InlineKeyboardMarkup(row_width=1).add(add_comment, check_comments, to_menu)

web_store = InlineKeyboardButton(f'Отзывы на {config.SITE}', url=config.LINK)
check_comments_menu = InlineKeyboardMarkup(row_width=1).add(web_store, to_menu)
