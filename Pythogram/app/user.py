from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
import os

from database.request import add_orders, add_platoon, get_platoon, add_soldier, get_soldier, get_order_by_index 
import app.keyboards as kb
from app.loading import ProgressBar
from config import PRICE, PAY_MESSAGE



# Путь к папке на рабочем столе
desktop_path = os.path.join(os.environ['HOME'], 'Desktop', 'photos')



class Reg(StatesGroup):
    platoon = State()

class Show(StatesGroup):
    showing = State()

class Making_order(StatesGroup):
    image = State()
    count = State()
    pay = State()
    save_order = State()
    proove_pay = State()
    final = State()
    


router = Router()
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    #Очищение состояний
    await state.clear()
    # Отправляем приветственное сообщение
    soldier = await get_soldier(message.from_user.id)
    
    if not soldier:
        await message.answer("Здравия желаю, солдат!")
        await message.answer("Напишите номер вашего взвода!\n\nНапример: Я из 931 взвода") 
        await state.set_state(Reg.platoon)
    else:
        platoon = await get_platoon(soldier.platoon_id)
        await message.answer(f'Здравия желаю, солдат {soldier.tg_name} из {platoon.name}а!', reply_markup=kb.main) 



@router.message(Reg.platoon)
async def reg_name(message: Message, state: FSMContext):
    #Добавление в бд
    platoon = int(''.join(filter(str.isdigit, message.text)))
    platoon = await add_platoon(platoon_name=(f"{platoon} Взвод"))
    await add_soldier(platoon_id=platoon.index,
                tg_id=message.from_user.id,
                tg_name=message.from_user.username)
    await state.clear()    
    await message.answer("Регистрация прошла успешно", reply_markup=kb.main)


@router.message(F.text == 'Посмотреть свои заказы')
async def get_showing_orders(message: Message, state: FSMContext):
    await message.answer("....................", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Show.showing)
    await message.answer("Выберите варианты", reply_markup=await kb.show_orders(message.from_user.id))



@router.callback_query(F.data.startswith('order_'), Show.showing)
async def skip(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Информация по заказу', reply_markup=ReplyKeyboardRemove())
    index = int(callback.data.split('_')[1])
    await state.clear()
    await callback.message.answer(f'`{await get_order_by_index(order_index=index)}`', parse_mode="Markdown", reply_markup=kb.main)
    #print(await get_order_by_index(order_index=index))


@router.callback_query(F.data.startswith('Menu'), Show.showing)
async def skip(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Menu', reply_markup=kb.main)


@router.message(F.text == 'Фото + 1 [25 руб]', Making_order.count)
async def handle_photo_inc_one(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(photo_count=data['photo_count']+1) 
    await state.update_data(add_price=data['add_price']+25) 
    data = await state.get_data()
    await message.answer(f"Всего Добавлено {data['photo_count']} на {data['add_price']}рублей", reply_markup=kb.photo_inc)

@router.message(F.text == 'Фото + 3 [60 руб]', Making_order.count)
async def handle_photo_inc_tree(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(photo_count=data['photo_count']+3) 
    await state.update_data(add_price=data['add_price']+60) 
    data = await state.get_data()
    await message.answer(f"Всего Добавлено {data['photo_count']} на {data['add_price']}рублей", reply_markup=kb.photo_inc)


@router.message(F.text == ('Продолжить'), Making_order.count)
async def handle_continue(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(Making_order.pay)
    await message.answer(f"И того к оплате: {data['add_price']}",reply_markup=kb.pay_men)

@router.message(F.text == ('Оплатить'), Making_order.pay)
async def handle_continue(message: Message, state: FSMContext):
    await message.answer(f"{PAY_MESSAGE}", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Making_order.save_order)
    ##########
    await message.answer(f"Все платеж увидели, информация поступила в базу данных \n\n Если нужна дополнительная информация восплользуйтесь подсказками в меню")
    await saving(message, state)
    
@router.message(F.text == ('Бля, ошибся че-то'), Making_order.pay)
async def handle_error(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Начнем сначала", reply_markup=kb.main)


@router.message(Making_order.save_order)
async def saving(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_orders(tg_id=message.from_user.id,
                     photo_path=data['photo_path'],
                     photo_count=data['photo_count'],
                     price=data['add_price'])
    await state.set_state(Making_order.proove_pay)
    await message.answer(f"Информация поступила в базу данных\nСкиньте скриншотом либо файлом информацию о платеже", reply_markup=ReplyKeyboardRemove())

@router.message(Making_order.proove_pay)
async def paying(message: Message, state: FSMContext):
    if message.photo:
        await message.answer("Сохраняем...")

        progress_bar = ProgressBar(message, total_steps=5, step_size=2)
        await progress_bar.start()

        await progress_bar.update()
        photo = message.photo[-1]  # Самая большая версия фото
        file_id = photo.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        file_name = os.path.basename(file_path)

        await progress_bar.update()
        # Создаем директорию, если она не существует
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)
        
        await progress_bar.update()
        # Путь для сохранения файла
        save_path = f'{desktop_path}/{file_name}'

        
        await progress_bar.update()
        # Скачиваем фото
        await message.bot.download_file(file_path, save_path)
        
        await progress_bar.update()
        # Сохраняем путь к файлу в состоянии
        await state.update_data(photo_path=save_path)


        await message.answer("Отлично, заказ сделан!", reply_markup=kb.main)

    # Проверяем, если это файл (например, изображение в другом формате)
    elif message.document:
        await message.answer("Cохраняем...")
        progress_bar = ProgressBar(message, total_steps=5, step_size=2)
        await progress_bar.start()

        await progress_bar.update()
        # Проверяем, является ли файл изображением
        file_name = message.document.file_name.lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        
        await progress_bar.update()
        # Проверяем, является ли файл изображением
        # Проверка расширения
        if any(file_name.endswith(ext) for ext in allowed_extensions):
            file_id = message.document.file_id
            file = await message.bot.get_file(file_id)
            file_path = file.file_path
            file_name = os.path.basename(file_path)
            
            await progress_bar.update()
            # Создаем директорию, если она не существует
            if not os.path.exists(desktop_path):
                os.makedirs(desktop_path)
        
            await progress_bar.update()
            # Путь для сохранения файла
            save_path = f'{desktop_path}/{file_name}'
            
            await progress_bar.update()
            # Скачиваем файл
            await message.bot.download_file(file_path, save_path)

            await message.answer(f"Отлично!")
            
            # Сохраняем путь к файлу в состоянии
            await state.update_data(photo_path=save_path)
        else:
            await message.answer("Файл может быть только в следующих форматах: jpg, jpeg, png, gif, bmp", reply_markup=kb.main)
            return
    else:
        await message.answer("Пожалуйста, отправьте изображение или файл с изображением.", reply_markup=kb.main)
        return

@router.message(F.text == 'Сделать заказ')
async def geting_order_1(message: Message, state: FSMContext):
    await message.answer("Скиньте фото c открытым декольте в рубашке, желательно без нижнего белья", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Making_order.image)


@router.message(Making_order.image)
async def reg_name(message: Message, state: FSMContext):
    if message.photo:
        await message.answer("Фотография обрабатывается.")

        progress_bar = ProgressBar(message, total_steps=5, step_size=2)
        await progress_bar.start()

        await progress_bar.update()
        photo = message.photo[-1]  # Самая большая версия фото
        file_id = photo.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        file_name = os.path.basename(file_path)

        await progress_bar.update()
        # Создаем директорию, если она не существует
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)
        
        await progress_bar.update()
        # Путь для сохранения файла
        save_path = f'{desktop_path}/{file_name}'

        
        await progress_bar.update()
        # Скачиваем фото
        await message.bot.download_file(file_path, save_path)
        
        await progress_bar.update()
        # Сохраняем путь к файлу в состоянии
        await state.update_data(photo_path=save_path)


        await message.answer("Фотография успешно сохранена.")

    # Проверяем, если это файл (например, изображение в другом формате)
    elif message.document:
        await message.answer("Файл обрабатывается.")
        progress_bar = ProgressBar(message, total_steps=5, step_size=2)
        await progress_bar.start()

        await progress_bar.update()
        # Проверяем, является ли файл изображением
        file_name = message.document.file_name.lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        
        await progress_bar.update()
        # Проверяем, является ли файл изображением
        # Проверка расширения
        if any(file_name.endswith(ext) for ext in allowed_extensions):
            file_id = message.document.file_id
            file = await message.bot.get_file(file_id)
            file_path = file.file_path
            file_name = os.path.basename(file_path)
            
            await progress_bar.update()
            # Создаем директорию, если она не существует
            if not os.path.exists(desktop_path):
                os.makedirs(desktop_path)
        
            await progress_bar.update()
            # Путь для сохранения файла
            save_path = f'{desktop_path}/{file_name}'
            
            await progress_bar.update()
            # Скачиваем файл
            #await message.bot.download_file(file_path, save_path)

            await message.answer(f"Файл успешно сохранен.")
            
            # Сохраняем путь к файлу в состоянии
            await state.update_data(photo_path=save_path)
        else:
            await state.clear()
            await message.answer("Файл может быть только в следующих форматах: jpg, jpeg, png, gif, bmp", reply_markup=kb.main)
            return
    else:
        await state.clear() 
        await message.answer("Пожалуйста, отправьте изображение или файл с изображением.", reply_markup=kb.main)
        return
    
    # Очищаем состояние
    await state.update_data(photo_count=3)
    await state.update_data(add_price=PRICE)
    data = await state.get_data()
    await state.set_state(Making_order.count)
    await message.answer(f"По умолчанию идет {data['photo_count']} фото за {data['add_price']}", reply_markup=kb.photo_inc)