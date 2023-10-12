from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton

'''   
        Создание обьект основной клавиатуры Пользователя и кнопок для основной клавиатуры Пользователя
'''
btn_1 = KeyboardButton(text='Список книг')
btn_2 = KeyboardButton(text='Поиск')
btn_3 = KeyboardButton(text='Корзина')


main_keyboard = ReplyKeyboardMarkup(keyboard=[[btn_1, btn_2], [btn_3]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)


'''   
        Создание кнопки для покупки книг
'''
btn_book = InlineKeyboardButton(text='Купить', callback_data='buy_all_books')
keyboard_book = InlineKeyboardMarkup(inline_keyboard=[[btn_book]])


'''   
        Создание кнопки для добавления в корзину и покупки
'''
btn_book_1 = InlineKeyboardButton(text='Купить сразу', callback_data='buy')
btn_book_2 = InlineKeyboardButton(text='В корзину', callback_data='in_basket')
keyboard_buy_basket = InlineKeyboardMarkup(inline_keyboard=[[btn_book_1, btn_book_2]])
