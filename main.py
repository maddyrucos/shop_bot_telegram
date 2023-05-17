from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from Functions import balance, catalog, comments
from states import Buy
from Database import database as db
import markups as mks

async def on_startup(_):
    await db.db_start() #инициализация базы данных

bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message):

    # Сбор необходимых данных пользователя
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    await db.create_profile(user_id, username, full_name) #Занесение пользователя в БД, при вводе /start

    # Вывод приветственного сообщения с Inline меню
    await bot.send_message(message.from_user.id, 'Добро пожаловать в лучший магазин!', reply_markup=mks.main_menu)

@dp.message_handler(commands=['admin'], state = '*')
async def admin(message: types.Message):

    # Проверка на наличие прав администратора
    await db.check_admin(bot, dp, message.from_user.username, message.from_user.id)


@dp.callback_query_handler(lambda c: c.data == 'main_menu', state = '*')
async def main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await Buy.default.set() #Стандартное состояние

    await callback_query.message.delete() #Удаление предыдущего сообщения, чтобы не засорять диалог

    await callback_query.message.answer('Главное меню', reply_markup=mks.main_menu)


@dp.callback_query_handler(lambda c: c.data == 'balance', state = '*')
async def main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.delete()

    #При нажатии Inline кнопки вызывается функция balance из файла balance
    await balance.balance(callback_query)


'''@dp.callback_query_handler(lambda c: c.data and 'deposit' in c.data, state = '*')
async def deposit(callback_query: types.CallbackQuery):

    await callback_query.message.delete()

    await Buy.deposit.set() #Состояние deposit, которой считывает текст сообщения от пользователя

    await callback_query.message.answer('Введите сумму пополнения')'''


'''@dp.message_handler(state=Buy.deposit)
async def get_deposit(message: types.Message):

    value = int(message.text)

    await payments.create_bill(message.from_user.id, value)

    await Buy.default.set()

    await message.answer('Запомнил сумму пополнения', reply_markup=mks.to_menu_only)'''


@dp.callback_query_handler(lambda c: c.data == 'catalog', state = '*')
async def main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.delete()

    #Создание клавиатуры для каталога
    catalog_cats = types.InlineKeyboardMarkup(row_width=1)
    db.cur.execute('SELECT good_category from goods') #Выделение всех категорий из таблицы с товарами
    cats = db.cur.fetchall()

    #Создание кнопок категорий без повторов
    for cat in set(cats):
        btn = types.InlineKeyboardButton(cat[0], callback_data=cat[0])
        catalog_cats.add(btn)
    catalog_cats.add(mks.to_menu)

    await callback_query.message.answer(text='Выберите категорию товара', reply_markup=catalog_cats)

    #Для каждой категории, принимая название за callback, выполняется функция show_categories, которая инициализирует хендлеры
    for callback in cats:

        await catalog.show_categories(bot, dp, callback[0])


@dp.callback_query_handler(lambda c: c.data == 'comment', state='*')
async def main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.delete()

    await callback_query.message.answer('В данном разделе Вы можете посмотреть отзывы пользователей о магазине, а также, оставить свой!', reply_markup=mks.comment_menu)


@dp.callback_query_handler(lambda c: c.data == 'check_comments', state='*')
async def main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.delete()

    await comments.watch_comments(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'add_comment', state='*')
async def main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.delete()

    await comments.add_comment(callback_query, dp)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup) #При запуске бота инициалиазируется БД