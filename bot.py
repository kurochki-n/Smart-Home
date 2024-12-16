from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import loop
from data.config import BOT_TOKEN
from handlers.router import router
from middlewares.check_whitelist import CheckWhitelist


async def main() -> None:
    bot = Bot(
        token=BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    
    dp.include_router(router)
    dp.message.middleware.register(CheckWhitelist())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=False, scheduler=scheduler)
  
    
if __name__ == "__main__":
    loop.run_until_complete(main())