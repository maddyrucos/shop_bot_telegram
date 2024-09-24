from aiogram import Router, types, F

from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from . import database as db
from . import markups as mks

transactions = Router()

@transactions.callback_query(F.data == 'buy')
async def buy(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = data['product']
    count = data['count']
    user = await sync_to_async(db.get_user_by_id, thread_sensitive=True)(callback.from_user.id)
    await sync_to_async(db.create_sale, thread_sensitive=True)(user,
                                                               product,
                                                               count=count,
                                                               cost=product.cost*count)
    try:
        if float(user.balance) < float(product.cost*count):
            amount = product.cost*count-user.balance
            await state.update_data(amount=amount)
            await callback.message.edit_caption(callback.id,
                  caption='У Вас недостаточно средств на балансе.\n'
                          f'Необходимо ещё {amount}',
                                                reply_markup=mks.topup_menu)

        else:
            await callback.message.edit_caption(callback.id,
                                                caption='Подтверждаете покупку?',
                                                reply_markup=mks.apply_transactions)

    except Exception as e:
        print(f'{e=}')
        await callback.message.answer('Возникла ошибка! Обратитесь к @madeezy')


@transactions.callback_query(F.data == 'apply_buy')
async def apply_buy(callback: types.CallbackQuery, state: FSMContext):
    user = await sync_to_async(db.get_user_by_id, thread_sensitive=True)(callback.from_user.id)
    data = await state.get_data()
    product = data['product']
    good = await sync_to_async(db.get_good, thread_sensitive=True)(product)
    if good != None:
        count = data['count']
        total_cost = count * product.cost
        if float(user.balance) >= float(total_cost):
            await sync_to_async(db.change_balance, thread_sensitive=True)(user, total_cost)
            sale = await sync_to_async(db.get_sale, thread_sensitive=True)(user, product, count, product.cost*count)
            if await sync_to_async(db.change_sale_status, thread_sensitive=True)(sale, 'paid'):
                media = types.InputMediaPhoto(media=types.FSInputFile(f'media/{product.photo}'),
                                              caption=f'{good}\n\n '
                                                      f'Нажмите /start')
                await callback.message.edit_media(media=media, reply_markup=None)
                await sync_to_async(db.delete_good, thread_sensitive=True)(good)

            else:
                await callback.message.answer('Возникла ошибка! Обратитесь к @madeezy')

        else:
            await callback.message.edit_caption(callback.id,
                                            caption='У Вас недостаточно средств на балансе.\n'
                                                    f'Необходимо ещё {product.cost - user.balance}',
                                            reply_markup=mks.topup_menu)

    else:
        await callback.message.edit_caption(callback.id,
                                            caption='Товар закончился!',
                                            reply_markup=mks.to_menu_only)