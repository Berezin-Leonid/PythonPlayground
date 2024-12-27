from database.model import async_session
from database.model import Platoon, Soldier, Orders, Blanked 
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from database.model import engine, AsyncSession
from prettytable import PrettyTable


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper


@connection
async def add_soldier(session,
                      tg_id: int,
                      tg_name: str,
                      platoon_id,):
    
    soldier = await session.scalar(select(Soldier).where(Soldier.tg_id == tg_id))
    if not soldier:
        soldier = Soldier(tg_id=tg_id, tg_name=tg_name, platoon_id=platoon_id)
        session.add(soldier)
        await session.commit()  # Подтверждаем добавление нового солдата
        print(f"Created new soldier with tg_id: {tg_id}")
    return soldier

@connection
async def get_soldier(session,
                      tg_id: int):
    soldier = await session.scalar(select(Soldier).where(Soldier.tg_id == tg_id))
    if not soldier: 
        return False
    return soldier
    

@connection
async def add_platoon(session,
                      platoon_name,):
    
    platoon = await session.scalar(select(Platoon).where(Platoon.name == platoon_name))
    if not platoon:
        platoon = Platoon(name=platoon_name)
        session.add(platoon)
        platoon_id = platoon.index
        await session.commit()  # Подтверждаем добавление нового взвода
        print(f"Created new platoon: {platoon_name}")
    platoon = await session.scalar(select(Platoon).where(Platoon.name == platoon_name))
    return platoon
@connection 
async def get_platoon(session,
                      platoon_id,):
    
    platoon = await session.scalar(select(Platoon).where(Platoon.index == platoon_id))
    if not platoon:
        return False
    return platoon

@connection
async def add_orders(session,tg_id, photo_path, photo_count, price):
    soldier = await get_soldier(tg_id=tg_id)
    order = Orders(soldier_id=soldier.index,
                   photo_path=photo_path,
                   photo_count=photo_count,
                   price=price)
    session.add(order)
    await session.commit()
    return order
    

@connection
async def get_orders(session,
                    tg_id,):
    soldier = await get_soldier(tg_id=tg_id)
    return await session.scalars(select(Orders).where(Orders.soldier_id == soldier.index))





class String:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text
@connection
async def get_order_by_index(session, order_index: int):
    """
    Получает заказ по его индексу и возвращает объект класса Orders.

    :param session: Сессия для работы с базой данных.
    :param order_index: Индекс заказа, который нужно получить.
    :return: Объект Orders или None, если заказ не найден.
    """
    order = await session.scalar(select(Orders).where(Orders.index == order_index))
 
    if order:
        # Создаем таблицу
        table = PrettyTable()
        
        # Устанавливаем заголовки столбцов
        table.field_names = ["Параметр", "Значение"]
        
        # Добавляем строки в таблицу
        table.add_row(["Кол-во фото", str(order.photo_count)])
        table.add_row(["Цена", str(order.price)])
        
        # Настроим выравнивание для колонок (по левому краю)
        table.align["Параметр"] = "l"
        table.align["Значение"] = "l"
        
        # Возвращаем отформатированную таблицу
        return String(str(table))
    else:
        return String("Заказ с таким индексом не найден.")

'''
@connection
async def check_and_create_orders(session,
                                 tg_id: int,
                                 platoon_name: str,
                                 photo_path: str,
                                 photo_count: int,
                                 make_name: int,
                                 price: int):
    result = await session.execute(select(Platoon).filter_by(name=platoon_name))
    platoon = result.scalars().first()

    # Если взвод не найден, создаем новый
    if not platoon:
    
    # Проверяем, существует ли солдат с указанным tg_id
    result = await session.execute(select(Soldier).filter_by(tg_id=tg_id))
    soldier = result.scalars().first()

    # Если солдат не найден, создаем нового

    # Создаем новый заказ для найденного солдата
    orders = Orders(
        soldier_id=soldier.index,
        photo_path=photo_path,
        photo_count=photo_count,
        make_name=make_name,  # Учтите, что make_name теперь integer
        price=price
    )
    session.add(orders)
    await session.commit()  # Подтверждаем добавление нового солдата
'''

import asyncio

async def main():
    # Замените на актуальные данные для теста
    await add_platoon(platoon_name="118 взвод")
    await add_platoon(platoon_name="117 взвод")
    await add_platoon(platoon_name="116 взвод")
    await add_platoon(platoon_name="115 взвод")
    await add_platoon(platoon_name="114 взвод")

    await add_soldier(tg_id=1, tg_name="@Bober28", platoon_id=1)
    await add_soldier(tg_id=5, tg_name="@Bober29", platoon_id=1)
    await add_soldier(tg_id=6, tg_name="@Bober30", platoon_id=1)
    await add_soldier(tg_id=7, tg_name="@Bober31", platoon_id=1)
    await add_soldier(tg_id=8, tg_name="@Bober32", platoon_id=1)
    await add_soldier(tg_id=9, tg_name="@Bober33", platoon_id=1)


    await add_soldier(tg_id=102, tg_name="@Bober1", platoon_id=2)
    await add_soldier(tg_id=202, tg_name="@Bober2", platoon_id=2)
    await add_soldier(tg_id=302, tg_name="@Bober3", platoon_id=2)
    await add_soldier(tg_id=402, tg_name="@Bober44", platoon_id=2)
    await add_soldier(tg_id=502, tg_name="@Bober4", platoon_id=2)
    await add_soldier(tg_id=602, tg_name="@Bober5", platoon_id=2)
    await add_soldier(tg_id=702, tg_name="@Bober6", platoon_id=2)
    await add_soldier(tg_id=802, tg_name="@Bober7", platoon_id=2)
    await add_soldier(tg_id=902, tg_name="@Bober8", platoon_id=2)

    await add_soldier(tg_id=103, tg_name="@Bober9", platoon_id=3)
    await add_soldier(tg_id=203, tg_name="@Bober10", platoon_id=3)
    await add_soldier(tg_id=303, tg_name="@Bober11", platoon_id=3)
    await add_soldier(tg_id=403, tg_name="@Bober12", platoon_id=3)
    await add_soldier(tg_id=503, tg_name="@Bober13", platoon_id=3)
    await add_soldier(tg_id=603, tg_name="@Bober14", platoon_id=3)
    await add_soldier(tg_id=703, tg_name="@Bober15", platoon_id=3)
    await add_soldier(tg_id=803, tg_name="@Bober16", platoon_id=3)
    await add_soldier(tg_id=903, tg_name="@Bober17", platoon_id=3)


    await add_soldier(tg_id=104, tg_name="@Bober18", platoon_id=4)
    await add_soldier(tg_id=204, tg_name="@Bober19", platoon_id=4)
    await add_soldier(tg_id=304, tg_name="@Bober20", platoon_id=4)
    await add_soldier(tg_id=404, tg_name="@Bober21", platoon_id=4)
    await add_soldier(tg_id=504, tg_name="@Bober22", platoon_id=4)
    await add_soldier(tg_id=604, tg_name="@Bober23", platoon_id=4)
    await add_soldier(tg_id=704, tg_name="@Bober24", platoon_id=4)
    await add_soldier(tg_id=804, tg_name="@Bober25", platoon_id=4)
    await add_soldier(tg_id=904, tg_name="@Bober26", platoon_id=4)



    '''
    await check_and_create_orders(
        tg_id=879,
        platoon_name='Alpha',
        photo_path='path/to/photo.jpg',
        photo_count=10,
        make_name=1,
        price=100
    )
    '''

if __name__ == "__main__":
    asyncio.run(main())