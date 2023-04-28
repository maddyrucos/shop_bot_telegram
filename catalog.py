from aiogram import types
from aiogram.dispatcher import FSMContext

from states import Buy
from database import cur, db

import config
import markups as mks

async def show_categories(bot, dp, cb):
    @dp.callback_query_handler(lambda c: c.data == cb, state='*')
    async def show_goods(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)

        await callback_query.message.delete()

        cur.execute(f'SELECT good_name, good_cost, good_category, good_description, good_photo FROM goods WHERE good_category == "{cb}"')
        callbacks = set(cur.fetchall())
        goods_markup = types.InlineKeyboardMarkup(row_width=1)
        for callback in callbacks:
            btn = types.InlineKeyboardButton(text = f'{callback[0]} - {callback[1]}', callback_data=callback[0])
            goods_markup.add(btn)

        back_to_categories = types.InlineKeyboardButton('⏪ Назад', callback_data='catalog')
        goods_markup.add(back_to_categories)

        await callback_query.message.answer(text='Выберите товар', reply_markup=goods_markup)

        await Buy.description.set()

        for callback in callbacks:

            await show_descrpition(bot, dp, callback)


async def show_descrpition(bot, dp, cb1):
    @dp.callback_query_handler(lambda c: c.data == cb1[0], state=Buy.description)
    async def buy(callback_query: types.CallbackQuery, state: FSMContext):

        await bot.answer_callback_query(callback_query.id)

        back_to_goods = types.InlineKeyboardButton('⏪ Назад', callback_data=cb1[2])
        apply = types.InlineKeyboardButton('✅ Купить', callback_data='apply_buy')
        apply_mk = types.InlineKeyboardMarkup(row_width=1).add(apply, back_to_goods)

        await callback_query.message.reply_photo(photo = cb1[4],caption=f'<b>Название:</b> {cb1[0]}\n\n<b>Стоимость:</b> {cb1[1]}\n\n<b>Описание:</b>\n{cb1[3]}', parse_mode = 'HTML', reply_markup = apply_mk)

        await callback_query.message.delete()

        cur.execute(f'SELECT good_name, good_cost, good_category FROM goods WHERE good_name == "{cb1[0]}"')
        good = cur.fetchone()

        await state.update_data(good = good)

        await Buy.buying.set()

        await buy_stuff(bot, dp)


async def buy_stuff(bot, dp):

    @dp.callback_query_handler(lambda c: c.data == 'apply_buy', state=Buy.buying)
    async def buy(callback_query: types.CallbackQuery, state: FSMContext):

        data = await state.get_data()
        good = data['good']

        await bot.answer_callback_query(callback_query.id)

        await callback_query.message.delete_reply_markup()

        cur.execute(f'SELECT balance FROM users WHERE user_id == "{callback_query.from_user.id}"')
        user_balance = cur.fetchone()

        if user_balance[0] >= good[1]:

            cur.execute(f'SELECT * FROM goods WHERE good_name == "{good[0]}"')
            good1 = cur.fetchall()

            try:

                new_user_balance = user_balance[0] - int(good1[0][2])

                cur.execute(f'UPDATE users SET balance = "{new_user_balance}" WHERE user_id == "{callback_query.from_user.id}"')
                db.commit()

                cur.execute(f'DELETE FROM goods WHERE good_id == "{good1[0][0]}"')
                db.commit()

                await callback_query.message.answer(text=f'Ваш код - {good1[0][3]}\nТекущий баланс - {new_user_balance}')
                await callback_query.message.answer(text=f'Если у Вас возникли трудности, пишите сюда - {config.admin}', reply_markup=mks.to_menu_only)

            except IndexError:

                await callback_query.message.answer("Товар закончился!", reply_markup=mks.to_menu_only)



        else:


            await callback_query.message.answer(text=f'Ваш баланс меньше, чем {good[1]}. Необходимо пополнить баланс на {good[1] - int(user_balance[0])}')

            await callback_query.message.answer(text=f'Если у Вас возникли трудности, пишите сюда - @madeezy', reply_markup=mks.to_menu_only)
