from aiogram import Router, types, F

from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from .states import User

from . import database as db
from . import markups as mks

catalog_router = Router()

@catalog_router.callback_query(F.data.startswith('catalog'))
async def catalog(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = await state.get_data()
    iter = data['iteration']
    path = str(callback_query.data)[8:]
    await state.update_data(path=path)
    categories, iteration = await sync_to_async(db.get_categories, thread_sensitive=True)(path, iter)
    if iteration != 'product':
        markup = mks.create_catalog(categories, path)
        await state.update_data(iteration=iteration)
        await callback_query.message.edit_caption(caption='Выберите категорию:', reply_markup=markup)
    else:
        markup = mks.create_catalog(categories, 'product')
        await callback_query.message.edit_caption(caption='Выберите товар:', reply_markup=markup)


@catalog_router.callback_query(F.data.startswith('product'))
async def catalog(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = await state.get_data()
    path=data['path']
    name=str(callback_query.data).split('_')[1]
    product = await sync_to_async(db.get_product, thread_sensitive=True)(name, path)
    if product != 0:
        await state.update_data(product=product)
        caption = f'Название: {product.name}\n\nЦена: {product.cost}\n\nОписание: {product.description}'
        media=types.InputMediaPhoto(media=types.FSInputFile(f'media/{product.photo}'),
                                    caption=caption)
        if product.is_counted:
            await callback_query.message.edit_media(media=media,
                                                    reply_markup=mks.counted_menu)
        else:
            await state.update_data(count=1)
            await callback_query.message.edit_media(media=media,
                                                    reply_markup=mks.product_menu)
    else:
        caption = 'Произошла ошибка'
        media = types.InputMediaPhoto(media=types.FSInputFile(f'media/{product.photo}'),
                                      caption=caption)
        await callback_query.message.edit_media(media,
                                                reply_markup=mks.to_main_menu)


@catalog_router.callback_query(F.data == 'count')
async def count(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(callback_query=callback_query)
    await callback_query.message.edit_caption(callback_query.id,
                                              caption=f'Введите количество')
    await state.set_state(User.count)


@catalog_router.message(User.count)
async def count(message: types.Message, state: FSMContext):
    try:
        count = float(message.text)
        await message.delete()
        await state.set_state(User.default)
        data = await state.get_data()
        callback_query = data['callback_query']
        await state.update_data(count=float(count))
        await callback_query.message.edit_caption(callback_query.id, caption=f'Количество: {count}')
        await callback_query.message.edit_reply_markup(callback_query.id, mks.product_menu)
    except Exception as e:
        print(e)
        await message.edit_caption('Возникла ошибка! Обратитесь к @madeezy')
