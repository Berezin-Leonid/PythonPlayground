from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.request import get_orders



main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сделать заказ')],
    [KeyboardButton(text='Посмотреть свои заказы')],
], resize_keyboard=True)


photo_inc = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Фото + 1 [25 руб]')],
    [KeyboardButton(text='Фото + 3 [60 руб]')],
    [KeyboardButton(text='Продолжить')],
], resize_keyboard=True)

pay_men = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Оплатить')],
    [KeyboardButton(text='Бля, ошибся че-то')],
], resize_keyboard=True)



async def show_orders(tg_id: int):
    all_orders = await get_orders(tg_id=tg_id)
    keyboard = InlineKeyboardBuilder()
    i = 0
    
    for order in all_orders:
        i += 1
        keyboard.add(InlineKeyboardButton(text=f"Заказ #{i}", callback_data=f'order_{order.index}'))
    if i == 0:
        keyboard.add(InlineKeyboardButton(text="Заказов нет, вернусь в меню", callback_data=f"Menu"))

    return keyboard.adjust(1).as_markup()
