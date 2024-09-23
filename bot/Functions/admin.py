from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions
from aiogram import types
import asyncio

from openpyxl import Workbook

from states import Admin
import markups as mks


async def admin(bot, dp, user_id, db):

    await Admin.default.set() # Передаем состояние админа, чтобы пользователи не имели доступа к этим хендлерам

    await bot.send_message(user_id, 'Вы админ', reply_markup=mks.admin_menu)

    cur = db.cursor() # Создаем курсор для рассылки сообщений

    # Рассылка сообщения всем пользователям
    @dp.callback_query_handler(lambda c: c.data and 'send_button' in c.data, state = Admin.default)
    async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)

        await bot.send_message(user_id, 'Введите сообщение')

        await Admin.sending_message.set() # Передаем состояние получения текста сообщения от пользователя

    @dp.message_handler(content_types=['text'], state = Admin.sending_message) # Принимаем сообщение, действует только при состоянии Admin.sending_message
    async def get_text(message: types.Message):

        text = message.text # Присваиваем текст сообщения от пользователя (администратора) в переменную, которую передадим как текст сообщения бота

        cur.execute('SELECT user_id FROM users') # Выделяем всех пользователей из базы данных

        user = cur.fetchall() # Помещаем всех пользователей из бд в переменную

        for row in user: # Для каждого ряда из списка пользователей

            # Создаем исключение с рядом возможных ошибок
            try:
                await bot.send_message(row[0], text)
            except exceptions.BotBlocked:
                print(f"Пользователь {user} заблокировал этого бота")
            except exceptions.ChatNotFound:
                print(f"Чат пользователя {user} не найден")
            except exceptions.RetryAfter as e:
                print(f"Апи отправило слишком много запросов, нужно немного подождать {e.timeout} секунд")
                await asyncio.sleep(e.timeout)
            except exceptions.TelegramAPIError:
                print(f"Ошибка Telegram API для пользователя {user}")

        await Admin.default.set() # Возвращаем состояние админа, чтобы сообщения не дублировались всем пользователям
        await bot.send_message(message.from_user.id, 'Сообщение отправлено всем пользователям',
                               reply_markup=mks.admin_menu)

    #выгрузка базы данных
    @dp.callback_query_handler(lambda c: c.data and 'download' in c.data, state = Admin.default)
    async def process_callback_button1(callback_query: types.CallbackQuery):

        await bot.answer_callback_query(callback_query.id)

        cur.execute('SELECT * FROM users')  # выбираем всю таблицу users
        data = cur.fetchall()  # передаем

        wb = Workbook()  # создаем воркбук для конвертирования бд
        ws = wb.active

        for row in data:
            ws.append(row)

        wb.save('users.xlsx')

        with open('users.xlsx', "rb") as file:
            await bot.send_document(callback_query.from_user.id, file, reply_markup=mks.admin_menu)

    #возврат в меню админа
    @dp.callback_query_handler(lambda c: c.data and 'admin' in c.data, state = Admin.default)
    async def process_callback_button1(callback_query: types.CallbackQuery):

        await bot.send_message(user_id, 'Меню администратора', reply_markup=mks.admin_menu)

    #Добавить товар
    @dp.callback_query_handler(lambda c: c.data and 'add_good' in c.data, state=Admin.default)
    async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):

        await Admin.cost.set()
        state_list = [Admin.cost, Admin.code, Admin.category, Admin.description, Admin.photo, Admin.end]
        new_good = []
        await state.update_data(new_good = new_good)
        await callback_query.message.answer('Введите название')

        for item in state_list:
           await add_good(item, dp, db, cur)


async def add_good(item, dp, db, cur):
    @dp.message_handler(content_types=['text'], state = item)
    async def get_data(message: types.Message, state: FSMContext):

        data = await state.get_data()
        good_properties_list = data['new_good']
        good_properties_list.append(message.text)
        await state.update_data(new_good=good_properties_list)
        good_property = str(item).split(":")[1]
        await message.answer(f'Введите {good_property}')
        await Admin.next()

    @dp.message_handler(content_types=['text'], state = Admin.end)
    async def check_data(message: types.Message, state: FSMContext):

        data = await state.get_data()
        new_good = data['new_good']
        new_good.append(message.text)
        await state.update_data(new_good=new_good)
        await Admin.apply.set()

        text = (f'Название - {new_good[0]}\n'
                f'Стоимость - {new_good[1]}\n'
                f'Код - {new_good[2]}\n'
                f'Катeгория - {new_good[3]}\n'
                f'Описание - {new_good[4]}\n'
                f'Фото - {new_good[5]}\n')

        await message.answer(text, reply_markup=mks.admin_add_good_menu)

    @dp.callback_query_handler(lambda c: c.data and 'apply_add_good' in c.data, state=Admin.apply)
    async def apply_add_good(callback_query: types.CallbackQuery, state: FSMContext):

        data = await state.get_data()
        new_good = data['new_good']
        cur.execute(f'INSERT INTO goods(good_name, good_cost, good_code, good_category, good_description, good_photo) '
                    f'VALUES ("{new_good[0]}", "{new_good[1]}", "{new_good[2]}", "{new_good[3]}", "{new_good[4]}", "{new_good[5]}")')
        db.commit()

        await callback_query.message.answer('Товар добавлен!', reply_markup=mks.admin_menu)
