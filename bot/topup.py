from aiogram import Router, types, F

from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from . import database as db
from . import markups as mks

from .states import User

topup = Router()

@topup.callback_query(F.data == 'topup')
async def buy(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(callback.id, caption='Выберите способ пополнения:', reply_markup=mks.topup_methods)


@topup.callback_query(F.data == 'manually')
async def manually(callback: types.CallbackQuery, state: FSMContext):
    method = await sync_to_async(db.get_topup_method, thread_sensitive=True)(callback.data)
    await callback.message.edit_caption(callback.id, caption=f'{method.description}\n\nВаш id - {callback.from_user.id}', reply_markup=mks.to_menu_only)



@topup.message(User.topup)
async def get_count(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        count = float(message.text)
        await message.delete()
        callback = data['callback_query']
        await message.edit_caption(callback.id, caption=f'Пополнение на {count}', reply_markup=mks)
    except:
        await message.edit_text('Введите сумму цифрами!')
