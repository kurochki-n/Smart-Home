import asyncio
import logging
import time
import subprocess

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.config import BOT_TOKEN
from src.handlers import router

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
  
    
if __name__ == "__main__":
    asyncio.run(main())