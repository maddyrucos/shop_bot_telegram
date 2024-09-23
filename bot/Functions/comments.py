from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram import types

from random import randint

from Database.database import cur, db
from states import Comment
import markups as mks

async def add_comment(callback_query, dp):

    rate_menu = InlineKeyboardMarkup(row_width=5)
    for i in range(1, 6):
        rate = InlineKeyboardButton(f'{i}', callback_data=i)
        rate_menu.insert(rate)

    await callback_query.message.answer('Выберите оценку', reply_markup = rate_menu)

    for rates in range(1, 6):
        get_rate(rates, dp)

def get_rate(rates, dp):
    @dp.callback_query_handler(lambda c: c.data == str(rates), state='*')
    async def show_rate(callback_query: types.CallbackQuery, state: FSMContext):

        await callback_query.message.delete()

        await Comment.comment.set()

        await state.update_data(rate = rates)

        await callback_query.message.answer('Напишите Ваше мнение о магазине')

    @dp.message_handler(content_types=['text'], state = Comment.comment)
    async def get_comm(message: types.Message, state: FSMContext):


        data = await state.get_data()
        rate = data['rate']

        text = message.text

        await state.update_data(comm = text)

        accept_btn = InlineKeyboardButton('Отправить', callback_data='apply_comment')
        accept_menu = InlineKeyboardMarkup(row_width=1).add(accept_btn, mks.to_menu)

        await Comment.basic.set()


        await message.answer(f'Ваша оценка: {rate}\nВаш комментарий:\n{text}', reply_markup= accept_menu)

    @dp.callback_query_handler(lambda c: c.data == 'apply_comment', state='*')
    async def show_rate(callback_query: types.CallbackQuery, state: FSMContext):

        await callback_query.message.delete()

        data = await state.get_data()

        cur.execute(f"INSERT INTO comments(user_id, username, comment, rate) VALUES ('{callback_query.from_user.id}', '{callback_query.from_user.username}', '{data['comm']}', '{data['rate']}')")
        db.commit()

        await callback_query.message.answer('Вы оставили отзыв!', reply_markup=mks.to_menu_only)


async def watch_comments(callback_query):

    comments = cur.execute('SELECT username, comment, rate FROM comments').fetchall()

    avg = 0

    for comment in comments:
        avg += comment[2]

    avg = avg/len(comments)
    r = randint(0, len(comments)-1)
    await callback_query.message.answer(f'Средняя оценка - {avg}\nСлучайный отзыв:\n\n<b>{comments[r][0]} - {int(comment[2])}/5</b>\n<i>{comments[r][1]}</i>', parse_mode = 'HTML', reply_markup = mks.check_comments_menu)