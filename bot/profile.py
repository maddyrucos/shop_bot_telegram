from aiogram import Router, types, F

from .states import User

from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from . import database as db, markups
from . import markups as mks

profile_router = Router()

@profile_router.callback_query(F.data=='profile')
async def profile(callback_query: types.CallbackQuery, state: FSMContext):
    profile = await sync_to_async(db.get_profile, thread_sensitive=True)(callback_query.from_user.id)
    profile_text = (f'<b>{str(profile["username"]).title()}</b>\n\n'
                    f'Покупок: {profile["sales"]}\n'
                    #f'Последняя покупка: {profile["last_sale"]}'
                    )
    media = types.InputMediaPhoto(
        media=types.FSInputFile(f'media/profile.png'),
                                    caption=profile_text, parse_mode='HTML')
    await callback_query.message.edit_media(media=media, reply_markup=mks.profile_menu)


@profile_router.callback_query(F.data=='code')
async def code(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_caption(callback_query.id, caption='Введите код:', reply_markup=None)
    await state.set_state(User.code)
    await state.update_data(callback_query=callback_query)


@profile_router.message(User.code)
async def code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    callback_query = data['callback_query']

    code = sync_to_async(db.check_code, thread_sensitive=True)(message.text)
    if code != None:
        await sync_to_async(db.change_balance, thread_sensitive=True)(code.amount)
        await callback_query.message.edit_caption(callback_query.id, caption='Код успешно активирован!', reply_markup=mks.to_menu_only)
    else:
        await callback_query.message.edit_caption(callback_query.id, caption='Код недействителен!', reply_markup=mks.to_menu_only)

    await message.delete()
    await state.set_state(User.default)