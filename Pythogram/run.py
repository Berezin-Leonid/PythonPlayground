import asyncio
from aiogram import Bot, Dispatcher
from database.model import async_main
from app.user import router
from config import TG_TOKEN

import sys
import os

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



async def main():
    await async_main()
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass