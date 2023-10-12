from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from filters_for_handler.Admin_filter import IsAdmin


router = Router()
admin_ids: list[int] = [108750276]
router.message.filter(IsAdmin(admin_ids))
# router.message.filter(F.from_user.id.in_(admin_ids))


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    author = State()
    description = State()
    price = State()


''' 
        Добавление новой книги
'''


@router.message(Command("new"))
async def add_book(message: Message, state: FSMContext):
    await state.set_state(FSMAdmin.name)
    await message.answer(text="Загрузите название:")


@router.message(FSMAdmin.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FSMAdmin.author)
    await message.answer('Введите автора книги:')


@router.message(FSMAdmin.author)
async def add_author(message: Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(FSMAdmin.description)
    await message.answer('Введите описание книги:')


@router.message(FSMAdmin.description)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(FSMAdmin.price)
    await message.answer('Введите цену книги:')


@router.message(FSMAdmin.price)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(FSMAdmin.photo)
    await message.answer('Загрузите фото:')


@router.message(FSMAdmin.photo, F.photo)
async def add_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    await state.clear()
    l = {}

    for key, value in data.items():
        l[key] = value
    print(l)
    await message.answer_photo(
        photo,
        f'Название: {l["name"]}\nАвтор: {l["author"]}\nОписание: {l["description"]}\nЦена:{l["price"]}'
    )


