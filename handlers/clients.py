from aiogram import F, Router
from config import bot
from aiogram.filters import Command, CommandStart
from data_base.buy_books_bd_for_books import get_all_books, search_for_book_in_bd
from data_base.buy_books_bd_users import new_user, update_basket, getting_information_from_the_cart
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, SuccessfulPayment, LabeledPrice, ContentType
from keyboards.buy_books_keyboard import main_keyboard, keyboard_book, keyboard_buy_basket


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Бот позволяет покупать христианскую литературу прямо в телеграме\n\n'
                         'Используйте клавиатуру для взаимодействия с Ботом\n\n'
                         'Если что-то не понятно отправь команду /help', reply_markup=main_keyboard)
    user_id: int = message.from_user.id
    ''' Добавление пользователя в Базу Данных'''
    new_user(user_id=user_id)


@router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer('Список книг - возможность посмотреть существующие книги\n'
                         'Поиск - возможность найти книгу по ее названию и автору\n'
                         'Корзина - возможность посмотреть книги которые вы выбрали для покупки')


@router.message(F.text == 'Список книг')
async def list_books(message: Message):
    all_books = get_all_books()
    print(all_books)
    for book in all_books:
        id, name, author, description, price, photo = book
        await message.answer_photo(photo=photo, caption=f'Название: {name}\n'
                             f'Автор: {author}\n'
                             f'Описание: {description}\n'
                             f'Цена: {price}',
                                   reply_markup=keyboard_buy_basket)


@router.message(F.text == 'Поиск')
async def search_book(message: Message):
    name = message.text[0]
    author = message.text[1]
    search_results = search_for_book_in_bd(name=name, author=author)
    id, name, author, description, price, photo = search_results
    await message.answer_photo(photo=photo, caption=f'Название: {name}\n'
                                                    f'Автор: {author}\n'
                                                    f'Описание: {description}\n'
                                                    f'Цена: {price}')


@router.message(F.text == 'Корзина')
async def basket_of_cart(message: Message):
    user_id = message.from_user.id
    books = getting_information_from_the_cart(user_id=user_id)
    books_for_buy = books[0].split(';')[0:-1]
    await message.answer(f'Общая стоимость книг в корзине - {books[1]}', reply_markup=keyboard_book)
    for book in books_for_buy:
        await message.answer(book)


# async def add_basket(callback: CallbackQuery):
#     user_id = callback.from_user.id
#     update_basket(user_id=user_id, name=, author=, price=)


@router.callback_query(F.data == 'buy_all_books')
async def process_buy_books(callback: CallbackQuery):
    user_id = callback.from_user.id
    total = getting_information_from_the_cart(user_id=user_id)
    await bot.send_invoice(chat_id=callback.from_user.id,
                           title='Buy book',
                           description='You can buy book special for you',
                           provider_token="381764678:TEST:67414",
                           currency='RUB',
                           payload='buy_book',
                           start_parameter='text',
                           prices=[
                               LabeledPrice(label="rub",
                                            amount=total[1]*100)]
                           )


@router.pre_checkout_query()
async def process_pre_check(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(SuccessfulPayment)
async def process_puy(message: Message):
    if message.successful_payment.invoice_payload == 'buy_book':
        await bot.send_message(message.chat.id, 'Successful!')


# Регистрируем хэндлеры
# def register_handler_clients(dp: Dispatcher):
#     dp.message.register(process_start_command, Command(commands='start'))
#     dp.message.register(process_help_command, Command(commands='help'))
#     dp.message.register(list_books, F.text == 'Список книг')
#     # dp.callback_query.register(add_basket, F.data == 'buy')
#     # dp.callback_query.register(process_buy_books, F.data == 'in_basket')
#     dp.message.register(search_book, F.text == 'Поиск')
#     dp.message.register(basket_of_cart, F.text == 'Корзина')
#     dp.callback_query.register(process_buy_books, F.data == 'buy_all_books')
#     dp.pre_checkout_query.register(process_pre_check)
#     dp.message.register(process_puy, SuccessfulPayment)
