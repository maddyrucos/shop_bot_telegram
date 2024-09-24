from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from asgiref.sync import sync_to_async

from . import markups as mks
from . import database as db
from . import config

from .catalog import catalog_router
from .transactions import transactions
from .profile import profile_router
from .topup import topup
from .states import User


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(User.count)
    await sync_to_async(db.create_profile, thread_sensitive=True)(message.from_user.id, message.from_user.username)
    photo = types.FSInputFile('media/menu.png')
    await message.answer_photo(photo=photo, caption='Добро пожаловать в наш магазин!\n', reply_markup=mks.to_menu_only)


@router.callback_query(F.data=='main_menu')
async def main_menu(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_caption(caption=f'🏠 Главное меню', reply_markup=mks.main_menu)


@router.callback_query(F.data=='to_catalog')
async def to_catalog(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    categories, iteration = await sync_to_async(db.get_categories, thread_sensitive=True)('', 0)
    await state.set_state(User.default)
    await state.update_data(iteration=iteration)
    markup = mks.create_catalog(categories, '')
    photo = types.FSInputFile('media/catalog.png')
    await callback_query.message.edit_media(media=types.InputMediaPhoto(media=photo, caption='Выберите категорию:'),reply_markup=markup)
    await callback_query.answer()


async def run_bot():
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(catalog_router)
    dp.include_router(profile_router)
    dp.include_router(topup)
    dp.include_router(transactions)

    await dp.start_polling(bot)


def main() -> None:
    import asyncio
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()